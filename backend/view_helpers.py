from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from c4sh.backend.models import Cashdesk
import re
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import logout
from c4sh.settings import EVENT_SUPERVISOR_IPS

def get_cashdesk(request=None, ip=None):
	if not request and not ip:
		raise Exception("get_cashdesk requires either a request object or the calling IP")
	if request:
		ip = request.META['REMOTE_ADDR']
	try:
		return Cashdesk.objects.get(ip=ip, active=True)
	except Cashdesk.DoesNotExist:
		messages.error(request, "This is not a valid cashdesk.")
		return HttpResponseRedirect(reverse('fail'))

def supervisor_required(func):
	"""
	This is the @supervisor_required decorator.
	It will check if the calling user is a supervisor, and if that is not case, throw errors.
	"""
	def _dec(request, *args, **kwargs):
		try:
			if request.user.is_superuser:
				if request.META['REMOTE_ADDR'] in EVENT_SUPERVISOR_IPS or Cashdesk.objects.get(ip=remote.META['REMOTE_ADDR'], allow_supervisor=True, active=True):
					pass
				else:
					messages.error(request, "You don't have supervisor rights.")
					return HttpResponseRedirect(reverse('fail'))
		except:
			raise Exception("Fix your configuration (EVENT_SUPERVISOR_IPS, Cashdesk objects). (DEBUG: backend)")
		return func(request, *args, **kwargs)
	return _dec