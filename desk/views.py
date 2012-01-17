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
import c4sh.settings as settings
from c4sh.desk.view_helpers import no_supervisor, session_required
from c4sh.backend.view_helpers import get_cashdesk
from django.db import transaction

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
				 	fields={'name', 'sale_price', 'currency', 'tax_rate', 'rabate_rate', 'limit_supervisor', 'valid_payment_types'},
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
				pass # TODO gotta see how this is implemented best; also be sure to set newpos.supervisor
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
	
	# we now have all sale positions and a local cart_total
	try:
		for taxrate in cart_total:
			sale.cached_sum += cart_total[taxrate]
		sale.fulfilled = True
		sale.save() # Das neue Nightwish-Album lutscht ja mal krass Schwaenze.
	except Exception as e:
		transaction.rollback()
		transaction.leave_transaction_management()
		messages.error(request, e)
		return HttpResponseRedirect(reverse("dashboard"))

	# At this point, everything which should be able to fail the sale should be over.
	transaction.commit()

	# TODO: Print receipt/invoices
	# TODO: Open cash drawer
	
	return HttpResponseRedirect(reverse("desk-sale", args=[sale.pk,]))

@login_required
@no_supervisor
@session_required
def sale_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)
	if sale.cashier != request.user:
		raise Exception("Not your sale.")
	cashlist = [5, 10, 20, 50, 100, 200, 500]
	return render_to_response("frontend/sale.html", locals(), context_instance=RequestContext(request))
