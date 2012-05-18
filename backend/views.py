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
from c4sh.backend.view_helpers import supervisor_required
import c4sh.settings as settings
from datetime import datetime

from c4sh.backend.forms import *

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
	
	#cashiers_active = User.objects.filter(is_staff=False)
	cashiers_active = CashdeskSession.objects.filter(cashier__is_active=True, cashier__is_staff=False, valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), is_logged_in=True)
	
	cashiers_inactive = User.objects.exclude(pk__in=CashdeskSession.objects.filter(cashier__is_active=True, cashier__is_staff=False, valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), is_logged_in=True).values("cashier__pk"))

	sessions_upcoming = CashdeskSession.objects.filter(Q(valid_from__gte=datetime.now()) | Q(valid_until__gte=datetime.now()) & Q(was_logged_in=False)).order_by('-valid_from')
	sessions_active = CashdeskSession.objects.filter(valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), was_logged_in=True, is_logged_in=True).order_by('-valid_from')
	sessions_old = CashdeskSession.objects.filter(Q(valid_until__lte=datetime.now()) | Q(was_logged_in=True) & Q(is_logged_in=False)).order_by('-valid_until')

	return render_to_response("backend/cashdesks.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def sale_reverse_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)
	sale.reversed_by = request.user
	sale.fulfilled = False
	sale.reversed = True
	sale.save()

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
	pdf.image('%ssigint-logo.png' % (settings.STATIC_ROOT), 280, 10, 1000*0.3, 580*0.3)
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
	pdf.text(150,220,"Ticket")
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
		pdf.set_font('Arial','',15)
		pdf.text(50, i, "%s x" % str(positions_merged[position]['amount']))
		pdf.text(150, i, positions_merged[position]['ticket'].name)
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

	pdf.set_font('Arial','',15)	
	pdf.text(20, i+60, "Day passes before session: %d" % session.day_passes_before)
	pdf.text(20, i+75, "Day passes after session: %d" % session.day_passes_after)
	pdf.text(20, i+91, "Total out: %d" % (session.day_passes_before - session.day_passes_after))
	pdf.text(20, i+110, "Full passes before session: %d" % session.full_passes_before)
	pdf.text(20, i+125, "Full passes after session: %d" % session.full_passes_after)
	pdf.text(20, i+140, "Total out: %d" % (session.full_passes_before - session.full_passes_after))


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

	if request.POST:
		form = EditSessionForm(request.POST, instance=session)
		if form.is_valid():
			"""if session.cashdesk.active_session == session:
				session.cashdesk.active_session = None
				session.cashdesk.save()"""
			form.save()
			messages.success(request, "The cashdesk session has been saved!")
	else:
		form = EditSessionForm(instance=session)

	# fetch positions which sale is marked as fulfilled and not reversed
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

	positions_for_template = []
	total_total = 0
	for position in positions_merged:
		positions_for_template.append(positions_merged[position])
		total_total = total_total + positions_merged[position]['total']


	# fetch positions which sale is marked as not fulfilled and reversed
	positions_reversed = SalePosition.objects.filter(sale__session=session, sale__fulfilled=False, sale__reversed=True)
	positions_reversed_merged = {}

	for position in positions_reversed:
		if not positions_reversed_merged.get(position.ticket.pk):
			positions_reversed_merged[position.ticket.pk] = {
				'ticket': position.ticket, 
				'amount': 1
			}
		else:
			positions_reversed_merged[position.ticket.pk]['amount'] = positions_reversed_merged[position.ticket.pk]['amount'] + 1

	positions_reversed_for_template = []
	for position in positions_reversed_merged:
		positions_reversed_for_template.append(positions_reversed_merged[position])

	return render_to_response("backend/cashdesks_session_edit.html", locals(), context_instance=RequestContext(request))


@login_required
@supervisor_required
def cashdesks_session_add_view(request):

	if request.POST:
		form = AddSessionForm(request.POST)
		if form.is_valid():

			cashdesk = form.cleaned_data['cashdesk']
			if cashdesk.active_session is not None:
				if cashdesk.active_session.valid_until > datetime.datetime.now():
					messages.error(request, "The cashdesk has an active session: %s" % cashdesk.active_session)
					return render_to_response("backend/cashdesks_session_add.html", locals(), context_instance=RequestContext(request))
				else:
					# delete active_session on cash desk now
					cashdesk.active_session = None
					cashdesk.save()

			cashier = pk=form.cleaned_data['cashier']
			if len(CashdeskSession.objects.filter(cashier=cashier, valid_from__lte=datetime.now(), valid_until__gte=datetime.now(), is_logged_in=True)) > 0:
				messages.error(request, "The cashier has an active session!")	
				return render_to_response("backend/cashdesks_session_add.html", locals(), context_instance=RequestContext(request))				

			form.save()
			messages.success(request, "The session has been successfully created!")
			return HttpResponseRedirect(reverse("backend-cashdesks"))
	else:
		form = AddSessionForm()
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