from django import template
from c4sh.backend.models import Cashdesk, CashdeskSession
from django.utils.timesince import timeuntil, timesince
import datetime

register = template.Library()

@register.filter
def cashdesk_session(session):
	try:
		cashdesk_pk = session["cashdesk"]
		cashdesk = Cashdesk.objects.get(pk=cashdesk_pk)
		cashdesk_session = cashdesk.active_session
		if (cashdesk_session.valid_until < datetime.datetime.now()):
			timeleft = timesince(cashdesk_session.valid_until) + " <span style=\"color:red\"><strong><u>overtime</u></strong></span>"
		else:
			timeleft = timeuntil(cashdesk_session.valid_until)
		return timeleft
	except:
		return "-"