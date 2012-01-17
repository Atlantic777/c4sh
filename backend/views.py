# -*- coding: utf8 -*-
import datetime, os, socket, re
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from c4sh.backend.models import *
from c4sh.desk.models import *
from c4sh.backend.view_helpers import supervisor_required
import c4sh.settings as settings

@login_required
def static_view(request, template, **args):
	if template == "fail.html":
		EVENT_C4SH_SUPPORT_CONTACT = settings.EVENT_C4SH_SUPPORT_CONTACT
	return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def dashboard_view(request):
	# aggregate static data
	event = settings.EVENT_NAME_SHORT
	dashtext = settings.EVENT_DASHBOARD_TEXT
	# aggregate statistics
	#  sold tickets
	#  cashdesks
	cashdesks_open = Cashdesk.objects.filter(active=True)
	sales = Sale.objects.all().order_by("-pk")
	return render_to_response("backend/dashboard.html", locals(), context_instance=RequestContext(request))

@login_required
@supervisor_required
def sale_detail_view(request, sale_id):
	sale = get_object_or_404(Sale, pk=sale_id)
	return render_to_response("backend/sale_detail.html", locals(), context_instance=RequestContext(request))