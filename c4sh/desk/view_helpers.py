from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from c4sh.backend.models import Cashdesk, CashdeskSession
import datetime
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import logout
from c4sh.settings import EVENT_SUPERVISOR_IPS
from c4sh.backend.view_helpers import get_cashdesk
from django.db import transaction

def reverse_sale(sale, supervisor):
	sale.reversed_by = supervisor
	sale.fulfilled = False
	sale.reversed = True
	sale.save()

	# reset honorary members so they can buy a ticket again
	for pos in sale.saleposition_set.all():
		pos.honorary_member = None
		pos.save()

	return True

### Decorators
def no_supervisor(func):
	"""
	This is the @no_supervisor decorator.
	It will check if the calling user is a supervisor, and if that is the case, will forward them
	to the backend (if backend logins are allowed from their machine) or log them out.
	"""
	def _dec(request, *args, **kwargs):
		try:
			if request.user.is_superuser:
				if request.META['REMOTE_ADDR'] in EVENT_SUPERVISOR_IPS or Cashdesk.objects.get(ip=remote.META['REMOTE_ADDR'], allow_supervisor=True, active=True):
					# User is authorized to use the backend on this machine.
					return HttpResponseRedirect(reverse('backend-dashboard'))
				else:
					logout(request)
					# logout user
					return HttpResponseRedirect(reverse('login'), ["fail=1"])
		except:
			raise Exception("Fix your configuration (EVENT_SUPERVISOR_IPS, Cashdesk objects). (DEBUG: desk) - Your IP is: %s", request.META['REMOTE_ADDR'])
		return func(request, *args, **kwargs)
	return _dec

def session_required(func):
	"""
	This will check if the calling user has a valid CashdeskSession.
	"""
	def _dec(request, *args, **kwargs):
		try:
			cashdesk = get_cashdesk(request)
			if not cashdesk:
				return HttpResponseRedirect(reverse('fail'))
			request.session["cashdesk"] = cashdesk.pk

			sessions = CashdeskSession.objects.filter(cashdesk=cashdesk, cashier=request.user, valid_from__lte=datetime.datetime.now(), cashier_has_ended=False)
			if len(sessions) <> 1:
				if len(sessions) < 1:
					messages.error(request, "There is no Cashdesk session scheduled for you at cashdesk %s" % cashdesk.name)
				else:
					messages.error(request, "There are too many Cashdesk session scheduled for you at cashdesk %s" % cashdesk.name)
				return HttpResponseRedirect(reverse('fail'))

			# check if there is an active session left at this cashdesk
			if cashdesk.active_session != None:
				if cashdesk.active_session.cashier != request.user:
					messages.error(request, "There is an active session left at cashdesk %s" % cashdesk.name)
					return HttpResponseRedirect(reverse('fail'))

			if request.user.is_superuser:
				if request.META['REMOTE_ADDR'] in EVENT_SUPERVISOR_IPS or Cashdesk.objects.get(ip=remote.META['REMOTE_ADDR'], allow_supervisor=True):
					# User is authorized to use the backend on this machine.
					return HttpResponseRedirect(reverse('backend-dashboard'))
				else:
					logout(request)
					return HttpResponseRedirect(reverse('login'), ["fail=1"])
		except:
			raise
			messages.error(request, "You cannot login here. Check your EVENT_SUPERVISOR_IPS and Cashdesk objects.")
			return HttpResponseRedirect(reverse('fail'))
		# check if session is already logged in
		session = sessions[0]
		if not session.was_logged_in:
			# first time logged in this session
			session.was_logged_in = True
		if not session.is_logged_in:
			# logged back in after logout
			session.is_logged_in = True
		try:
			cashdesk.active_session = session
			cashdesk.save()
			session.save()
		except:
			raise
		request.session["cashdesksession"] = session.pk
		# TODO check if session expires soon, set message in that case

		return func(request, *args, **kwargs)
	return _dec

### Context processors
"""
# does not currently work due to the nature the transactionmiddleware works.
# will throw "This code isn't under transaction management"
class SaleContextProcessor():
	def __init__(self, request):
		self.request = request

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_value, traceback):
		transaction.rollback()
		transaction.leave_transaction_management()
		messages.error(request, exc_value)
		return HttpResponseRedirect(reverse("dashboard"))
"""
