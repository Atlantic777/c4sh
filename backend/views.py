# -*- coding: utf8 -*-
import datetime, os, socket, re
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from c4sh.backend.models import *
from c4sh.desk.models import *
from c4sh.desk.view_helpers import reverse_sale
from c4sh.backend.view_helpers import supervisor_required
import c4sh.settings as settings
from datetime import datetime

from c4sh.backend.forms import *

from c4sh.desk.tools import print_session_end_bon, open_drawer

@login_required
def static_view(request, template, **args):
	if template == "fail.html":
		EVENT_C4SH_SUPPORT_CONTACT = settings.EVENT_C4SH_SUPPORT_CONTACT
	return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def sales_view(request):
	sales = Sale.objects.all().order_by("-pk")
	return render_to_response("backend/sales.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def dashboard_view(request):
	# aggregate static data
	event = settings.EVENT_NAME_SHORT
	dashtext = settings.EVENT_DASHBOARD_TEXT
	# aggregate statistics
	#  sold tickets
	tickets_sold = len(SalePosition.objects.all())
	#  cashdesks
	cashdesks_open = len(Cashdesk.objects.filter(Q(active=True) & ~Q(active_session=None)))
	cashdesks = len(Cashdesk.objects.filter())

	sales = Sale.objects.all().order_by("-pk")
	return render_to_response("backend/dashboard.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def cashdesks_view(request):
	event = settings.EVENT_NAME_SHORT
	cashdesks_open = Cashdesk.objects.filter(Q(active=True) & ~Q(active_session=None))
	cashdesks_closed = Cashdesk.objects.filter(Q(active=True) & Q(active_session=None))
	cashdesks_inactive = Cashdesk.objects.filter(active=False)

	cashiers_active = CashdeskSession.objects.filter(cashier__is_active=True, cashier__is_staff=False, valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), is_logged_in=True)

	cashiers_inactive = User.objects.exclude(pk__in=CashdeskSession.objects.filter(cashier__is_active=True, cashier__is_staff=False, valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), is_logged_in=True).values("cashier__pk"))

	sessions_upcoming = CashdeskSession.objects.filter(Q(valid_from__gte=datetime.now()) | Q(valid_until__gte=datetime.now()) & Q(was_logged_in=False)).order_by('-valid_from')

	sessions_active = CashdeskSession.objects.filter(valid_from__lte=datetime.now(), cashier_has_ended=False, was_logged_in=True, is_logged_in=True).order_by('-valid_from')

	sessions_paused = CashdeskSession.objects.filter(valid_from__lte=datetime.now(), was_logged_in=True, is_logged_in=False, cashier_has_ended=False).order_by('-valid_from')

	sessions_old = CashdeskSession.objects.filter(Q(was_logged_in=True) & Q(is_logged_in=False) & Q(supervisor_after=None) & Q(cashier_has_ended=True)).order_by('-valid_until')

	sessions_archive = CashdeskSession.objects.filter(~Q(supervisor_after=None)).order_by('-valid_until')

	return render_to_response("backend/cashdesks.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def sale_reverse_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)
	reverse_sale(sale, request.user)

	messages.success(request, "Sale has been successfully marked as reversed!")
	return HttpResponseRedirect(reverse("backend-sale-detail", args=[sale_id,]))

@login_required
@supervisor_required
def sale_detail_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)

	cashdesks = Cashdesk.objects.all()

	return render_to_response("backend/sale_detail.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def cashdesks_session_report_view(request, session_id):
	session = get_object_or_404(CashdeskSession, pk=session_id)

	from fpdf import FPDF
	import time
	from django.template.defaultfilters import floatformat
	from os import remove

	pdf=FPDF('P', 'pt', 'A4')
	pdf.add_page()
	pdf.set_right_margin(0)

	# print logo
	pdf.image(settings.STATIC_ROOT+'/'+settings.EVENT_REPORT_LOGO, 400, 10, 1920*0.1, 1600*0.1)
	pdf.set_font('Arial','B',50)
	pdf.text(20,60,"%s" % settings.EVENT_NAME_SHORT)

	pdf.set_font('Arial','B',20)
	pdf.text(20,100,"Cashdesk Session Report")

	pdf.set_font('Arial','',15)
	pdf.text(20,130,"#%d, %s - Cashier: %s" % (session.pk, session.cashdesk.name, session.cashier))
	pdf.set_font('Arial','',10)
	pdf.text(20,145,"%s - %s" % (session.valid_from, session.valid_until))

	# print ticket table
	pdf.set_font('Arial','B',15)
	pdf.text(80,220,"Ticket")
	pdf.text(330,220,"Price single")
	pdf.text(500,220,"Total")

	i = 250
	positions = SalePosition.objects.filter(sale__session=session, sale__fulfilled=True, sale__reversed=False)
	positions_merged = {}

	for position in positions:
		if not positions_merged.get(position.ticket.pk):
			positions_merged[position.ticket.pk] = {
				'ticket': position.ticket,
				'amount': 1,
				'total': position.ticket.sale_price
			}
		else:
			positions_merged[position.ticket.pk]['amount'] = positions_merged[position.ticket.pk]['amount'] + 1
			positions_merged[position.ticket.pk]['total'] = positions_merged[position.ticket.pk]['amount'] * positions_merged[position.ticket.pk]['ticket'].sale_price

	total_total = 0
	for position in positions_merged:
		pdf.set_font('Arial','',11)
		pdf.text(50, i, "%s x" % str(positions_merged[position]['amount']))
		pdf.text(80, i, positions_merged[position]['ticket'].name)
		pdf.text(330, i, "%s EUR" % str(positions_merged[position]['ticket'].sale_price))
		pdf.text(500, i, "%s EUR" % str(positions_merged[position]['total']))
		i = i + 20
		total_total = total_total + positions_merged[position]['total']

	pdf.set_font('Arial','',15)
	pdf.text(20, i+20, "Change before session: %s EUR" % session.change)
	pdf.text(20, i+40, "Received: %s EUR" % total_total)
	pdf.text(20, i+60, "==============================")
	pdf.set_font('Arial','B',15)
	pdf.text(20, i+80, "%s EUR" % ((total_total) + (session.change)))



	# reversed positions
	positions_reversed = SalePosition.objects.filter(sale__session=session, sale__fulfilled=False, sale__reversed=True)
	positions_reversed_merged = {}

	if len(positions_merged) > 0:
		i = i + 125
		pdf.set_font('Arial','B',15)
		pdf.text(20, i,"Reversed tickets")
		i = i + 25

	for position in positions_reversed:
		if not positions_reversed_merged.get(position.ticket.pk):
			positions_reversed_merged[position.ticket.pk] = {
				'ticket': position.ticket,
				'amount': 1
			}
		else:
			positions_reversed_merged[position.ticket.pk]['amount'] = positions_reversed_merged[position.ticket.pk]['amount'] + 1

	for position in positions_reversed_merged:
		pdf.set_font('Arial','',15)
		pdf.text(50, i, "%s x" % str(positions_reversed_merged[position]['amount']))
		pdf.text(150, i, positions_reversed_merged[position]['ticket'].name)
		i = i + 20

	####

	if len(positions_merged) > 0:
		i = i + 50
	else:
		i = i + 150

	if not session.drawer_sum:
		session.drawer_sum = "NOT YET SAVED"
	if not session.drawer_sum_ok:
		session.drawer_sum_ok = "NOT YET SAVED"
	pdf.text(20, i+10, "Money in cashdesk: %s EUR" % session.drawer_sum)
	pdf.text(20, i+30, "OK? %s" % session.drawer_sum_ok)

	### passes ###

	passes = CashdeskSessionPass.objects.filter(session=session)

	pdf.set_font('Arial','',15)
	ii = 60
	for p in passes:
		pdf.text(20, i+ii, "%s before session: %d" % (p.pass_type.name, p.before_session))
		try:
			pdf.text(20, i+ii+18, "%s after session: %d" % (p.pass_type.name, p.after_session))
		except:
			pass
		try:
			pdf.text(20, i+ii+36, "Total out: %d" % (p.before_session - p.after_session))
		except:
			pass
		ii += 22

	if session.supervisor_after == None:
		session.supervisor_after = session.supervisor_before

	pdf.set_font('Arial','',15)
	pdf.text(20, 800, "------------------------------------------")
	pdf.text(20, 815, "Supervisor: %s %s" % (session.supervisor_after.first_name, session.supervisor_after.last_name))

	pdf.set_font('Arial','',15)
	pdf.text(300, 800, "------------------------------------------")
	pdf.text(300, 815, "Cashier: %s %s" % (session.cashier.first_name, session.cashier.last_name))

	response = HttpResponse(mimetype="application/pdf")
	response['Content-Disposition'] = 'inline; filename=%s-%s.pdf' % ('sigint-session-report', session.pk)
	response.write(pdf.output('', 'S'))

	return response

@login_required
@supervisor_required
def cashdesks_session_edit_view(request, session_id):
	session = get_object_or_404(CashdeskSession, pk=session_id)

	# passes
	passes = CashdeskSessionPass.objects.filter(session=session)

	if request.POST:
		form = EditSessionForm(request.POST, instance=session)
		if form.is_valid():
			"""if session.cashdesk.active_session == session:
				session.cashdesk.active_session = None
				session.cashdesk.save()"""

			# saving pass stuff here
			pass_data = []
			for p in passes:
				try:
					if request.POST.get('passes_before[%d]' % p.pk):
						before_session = int(request.POST.get('passes_before[%d]' % p.pk))
					else:
						before_session = None

					if request.POST.get('passes_after[%d]' % p.pk):
						after_session = int(request.POST.get('passes_after[%d]' % p.pk))
					else:
						after_session = None

					if before_session <= 0:
						messages.error(request, "Error: The amount of passes before the session starts cannot be <= 0!")
						return render_to_response("backend/cashdesks_session_edit.html", locals(), context_instance=RequestContext(request))

					pass_data.append({'pass': p, 'before_session': before_session, 'after_session': after_session})
				except:
					messages.error(request, "An error occurred while saving the pass data. Please report this to %s as this should never happen!" % settings.EVENT_C4SH_SUPPORT_CONTACT)
					return render_to_response("backend/cashdesks_session_edit.html", locals(), context_instance=RequestContext(request))

			for p in pass_data:
				p['pass'].before_session = p['before_session']
				p['pass'].after_session = p['after_session']
				p['pass'].save()

			form.save()
			messages.success(request, "The cashdesk session has been saved!")
	else:
		form = EditSessionForm(instance=session)


	# moved all the fancy stuff© to CashdeskSession model

	positions = session.get_merged_positions()
	positions_reversed = session.get_reversed_positions()

	total = positions['total']

	positions_for_template = []
	for position in positions['positions']:
		positions_for_template.append(positions['positions'][position])

	positions_reversed_for_template = []
	for position in positions_reversed['positions']:
		positions_reversed_for_template.append(positions_reversed['positions'][position])

	return render_to_response("backend/cashdesks_session_edit.html", locals(), context_instance=RequestContext(request))


@login_required
@supervisor_required
def cashdesks_session_add_view(request):

	passes = Pass.objects.filter(is_active=True)

	if request.POST:
		form = AddSessionForm(request.POST)
		if form.is_valid():

			# check what kind of passes have been given to the cashier
			passes_given = []
			for p in passes:
				try:
					if int(request.POST.get('passes_before[%d]' % p.pk)) > 0:
						passes_given.append({'pass': p, 'amount': int(request.POST.get('passes_before[%d]' % p.pk))})
				except:
					pass

			cashdesk = form.cleaned_data['cashdesk']
			# we ignore this stuff as the session ends now after cashier logout
			"""if cashdesk.active_session is not None:
				if cashdesk.active_session.valid_until > datetime.now():
					messages.error(request, "The cashdesk has an active session: %s" % cashdesk.active_session)
					return render_to_response("backend/cashdesks_session_add.html", locals(), context_instance=RequestContext(request))
				else:
					# delete active_session on cash desk now
					cashdesk.active_session = None
					cashdesk.save()

					# open cash drawer
					open_drawer(cashdesk.receipt_printer_name)
					print_session_end_bon(cashdesk.receipt_printer_name)"""

			cashier = pk=form.cleaned_data['cashier']
			if len(CashdeskSession.objects.filter(cashier=cashier, valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), is_logged_in=True)) > 0:
				messages.error(request, "The cashier has an active session!")
				return render_to_response("backend/cashdesks_session_add.html", locals(), context_instance=RequestContext(request))

			cashdesk_session = form.save()

			# save passes associacted with this cashdesk session
			for p in passes_given:
				CashdeskSessionPass(pass_type=p['pass'], session=cashdesk_session, before_session=p['amount']).save()

			messages.success(request, "The session has been successfully created!")
			return HttpResponseRedirect(reverse("backend-cashdesks"))
	else:
		form = AddSessionForm(initial={"valid_from": datetime.now()})
	return render_to_response("backend/cashdesks_session_add.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def cashdesks_cashier_add_view(request):

	if request.POST:
		form = AddCashierForm(request.POST)
		if form.is_valid():
			user = User(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
			user.set_password(form.cleaned_data['password2'])
			user.save()
			user_profile = UserProfile(user=user, created_by=request.user)
			user_profile.save()
			messages.success(request, "The cashier has been successfully created!")
			return HttpResponseRedirect(reverse("backend-cashdesks"))
	else:
		form = AddCashierForm()
	return render_to_response("backend/cashdesks_cashier_add.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def monitor_view(request):
	now = datetime.now()
	cashdesks = Cashdesk.objects.filter(active=True)
	return render_to_response("backend/monitor.html", locals(), context_instance=RequestContext(request))
