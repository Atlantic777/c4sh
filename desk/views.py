# -*- coding: utf8 -*-
import datetime, os, socket, re, datetime
from django.core import serializers
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from c4sh.backend.models import *
from c4sh.desk.models import *
from c4sh.preorder.models import *
import c4sh.settings as settings
from c4sh.desk.view_helpers import no_supervisor, session_required
from c4sh.backend.view_helpers import get_cashdesk
from django.db import transaction
from django.db.models import Q
from c4sh.desk.tools import print_receipt, open_drawer


@login_required
def static_view(request, template, **args):
	return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
@no_supervisor
@session_required
def dashboard_view(request):
	"""
	This is the main seller action. Tickets are being sold here.
	"""
	# TODO: honor validity times of tickets in selection
	tickets = Ticket.objects.filter(active=True, deleted=False)
	tickets_json = serializers.serialize('json', tickets,
				 	fields=('name', 'sale_price', 'currency', 'tax_rate', 'rabate_rate', 'limit_supervisor', 'limit_honorary_member', 'valid_payment_types'),
					ensure_ascii=False)
	#payment_types_json = serializers.serialize('json', PaymentType.objects.all(), ensure_ascii=False)
	return render_to_response("frontend/dashboard.html", locals(), context_instance=RequestContext(request))

@login_required
@no_supervisor
@session_required
def sell_action(request):
	"""
	This action should:
		* Calculate the price total (including tax total and rabate total) -- DONE (excl. rabate)
		* Check that supervisor authorization was done
		* Write a Sale object and regarding SalePosition objects -- DONE
		* Print an receipt/invoice if neccessary by calling printReceipt(saleid) etc
		* Open the local cash drawer (if EVENT_DRAWER is set)
		* Display a intermediate page until cash drawer is closed (or a button is pressed) which has a change calculator -- DONE
	Note: This action needs to be in a single transaction. This is now the case thanks to Django's TransactionMiddleware.
	"""
	ticketcache = {}
	cart_total = {}

	try:
		cds = CashdeskSession.objects.get(pk=request.session["cashdesksession"])
	except CashdeskSession.DoesNotExist:
		messages.error(request, "Your session seems to be over")
		return HttpResponseRedirect(reverse("fail"))
	sale = Sale(cashier=request.user, cashdesk=get_cashdesk(request=request), session=cds, cached_sum=0, time=datetime.datetime.now())
	sale.save() # we need a primary key

	for ticketid in request.POST.getlist("position"):
		ticket_list = request.POST.getlist("position")

		if not ticketcache.get(ticketid):
			ticketcache[ticketid] = get_object_or_404(Ticket, pk=ticketid, active=True, deleted=False) # sale time restriction will be honored later to give an useful error
		cart_total[ticketcache[ticketid].tax_rate] = cart_total.get(ticketcache[ticketid].tax_rate, 0) + ticketcache[ticketid].sale_price # taxes included
		newpos = SalePosition(sale=sale, ticket=ticketcache[ticketid])
		# TODO implement local overrides of sale price etc
		# Check requirements -- NOTE: they cause to fail the complete transaction! nothing will be sold!
		try:
			# Check for time restriction
			if ticketcache[ticketid].limit_timespan:
				if not ticketcache[ticketid].valid_from < datetime.datetime.now() < ticketcache[ticketid].valid_until:
					raise Exception("You can't sell %s before %s or after %s." % (ticketcache[ticketid].name, ticketcache[ticketid].valid_from, ticketcache[ticketid].valid_until))

			# Check for supervisor:
			if ticketcache[ticketid].limit_supervisor:
				shall_pass = False
				# check if we have supervisor_auth_code in POST
				if request.POST.get("supervisor_auth_code"):
					try:
						supervisor = User.objects.get(userprofile__supervisor_auth_code=request.POST.get("supervisor_auth_code"), is_staff=True, userprofile__supervisor_auth_code__isnull=False)
						newpos.supervisor = supervisor
						shall_pass = True
					except User.DoesNotExist:
						messages.error(request, "Invalid supervisor auth code or supervisor not found!")

				if not shall_pass:
					transaction.rollback()

					# get all items from the basket to redisplay it
					try:
						tickets = Ticket.objects.filter(pk__in=request.POST.getlist("position"))
					except Ticket.DoesNotExist:
						pass

					try:
						preorder_tickets = PreorderPosition.objects.filter(uuid__in=request.POST.getlist("uuid"))
					except PreorderPosition.DoesNotExist:
						pass

					return render_to_response("frontend/sale_supervisor.html", locals(), context_instance=RequestContext(request))

			# Decided against checking for venue limit here.
		except Exception as e:
			transaction.rollback()
			transaction.leave_transaction_management()
			messages.error(request, e)
			return HttpResponseRedirect(reverse("dashboard"))
		# Passed requirements, let's sell this thing
		try:
			newpos.save()
		except Exception as e:
			transaction.rollback()
			transaction.leave_transaction_management()
			messages.error(request, e)
			return HttpResponseRedirect(reverse("dashboard"))

	# process preorders
	for uuid in request.POST.getlist("uuid"):

		ticket_position = get_object_or_404(PreorderPosition, uuid=uuid)
		ticket = get_object_or_404(Ticket, pk=ticket_position.ticket.backend_id, active=True, deleted=False)

		cart_total[ticket.tax_rate] = cart_total.get(ticket.tax_rate, 0) + ticket.sale_price # taxes included
		newpos = SalePosition(sale=sale, ticket=ticket, uuid=uuid)

		try:
			if ticket_position.redeemed == True:
				raise Exception("The Preorder Code %s has already been redeemed." % uuid)

			if ticket_position.preorder.paid != True:
				raise Exception("The Preorder %s has not yet been marked as paid." % uuid)

		except Exception as e:
			transaction.rollback()
			transaction.leave_transaction_management()
			messages.error(request, e)
			return HttpResponseRedirect(reverse("dashboard"))
		# Passed requirements, let's sell this thing
		try:
			newpos.save()
			ticket_position.redeemed = True
			ticket_position.save()
		except Exception as e:
			transaction.rollback()
			transaction.leave_transaction_management()
			messages.error(request, e)
			return HttpResponseRedirect(reverse("dashboard"))

	# we now have all sale positions and a local cart_total
	# therefore, we need to check for tickets which require honorary member identification
	# we need a sale position PK for this, that's why we're doing this last
	all_positions = SalePosition.objects.filter(sale=sale)
	for pos in all_positions:
		if pos.ticket.limit_honorary_member:
			shall_pass = False

			# check if we have supervisor_auth_codes in POST
			if request.POST.get("honoary_member_number_%d" % pos.pk):
				honorary_member_number = request.POST.get("honoary_member_number_%d" % pos.pk)
				try:
					honorary_member = HonoraryMember.objects.get(Q(membership_number=honorary_member_number) & Q(saleposition=None))

					pos.honorary_member = honorary_member
					pos.save()
					shall_pass = True
				except HonoraryMember.DoesNotExist:
					messages.error(request, "Invalid honoary member identification or not found or has already been used: #%s" % honorary_member_number)
					shall_pass = False

			if not shall_pass:
				transaction.rollback()

				# did we need a supervisor auth code?
				supervisor_auth_code = request.POST.get("supervisor_auth_code")

				# get all items from the basket to redisplay it
				positions = all_positions
				return render_to_response("frontend/sale_honorary_member.html", locals(), context_instance=RequestContext(request))

	# save everything!1
	try:
		for taxrate in cart_total:
			sale.cached_sum += cart_total[taxrate]
		sale.save() # Das neue Nightwish-Album lutscht ja mal krass Schwaenze.
	except Exception as e:
		transaction.rollback()
		transaction.leave_transaction_management()
		messages.error(request, e)
		return HttpResponseRedirect(reverse("dashboard"))

	# At this point, everything which should be able to fail the sale should be over.
	transaction.commit()

 	# sale fulfilled
	sale.fulfilled = True
	sale.save()

	print_receipt(sale, cds.cashdesk.receipt_printer_name)

	return HttpResponseRedirect(reverse("desk-sale", args=[sale.pk,]))

@login_required
def logout_view(request):
	from django.contrib.auth import logout as auth_logout

	cashdesk = get_cashdesk(request)
	if cashdesk:

		# open cash drawer
		open_drawer(cashdesk.receipt_printer_name)

		sessions = CashdeskSession.objects.filter(cashdesk=cashdesk, cashier=request.user, valid_from__lte=datetime.datetime.now(), valid_until__gte=datetime.datetime.now())
		try:
			session = sessions[0]
			session.is_logged_in = False
			session.save()
			cashdesk.active_session = None
			cashdesk.save()
		except:
			pass

	auth_logout(request)
	return HttpResponseRedirect(reverse("dashboard"))

@login_required
@no_supervisor
@session_required
def reverse_sale_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)
	if sale.cashier != request.user:
		raise Exception("Not your sale.")

	# check if we have supervisor_auth_code in POST
	if request.POST.get("supervisor_auth_code"):
		try:
			supervisor = User.objects.get(userprofile__supervisor_auth_code=request.POST.get("supervisor_auth_code"), is_staff=True, userprofile__supervisor_auth_code__isnull=False)
			sale.reversed_by = supervisor
			sale.fulfilled = False
			sale.reversed = True
			sale.save()

			messages.success(request, "Sale has been successfully marked as reversed!")
			return HttpResponseRedirect(reverse("dashboard"))

		except User.DoesNotExist:
			messages.error(request, "Invalid supervisor auth code or supervisor not found!")

	return render_to_response("frontend/reversal_supervisor.html", locals(), context_instance=RequestContext(request))


@login_required
@no_supervisor
@session_required
def sale_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)
	if sale.cashier != request.user:
		raise Exception("Not your sale.")
	cashlist = [25, 50, 75, 100, 125, 150]
	return render_to_response("frontend/sale.html", locals(), context_instance=RequestContext(request))
