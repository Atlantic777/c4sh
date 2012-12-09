from django import template
from c4sh.backend.models import Cashdesk, CashdeskSession
from django.utils.timesince import timeuntil

register = template.Library()

@register.filter
def cashdesk_session(session):
	try:
		cashdesk_pk = session["cashdesk"]
		cashdesk = Cashdesk.objects.get(pk=cashdesk_pk)
		cashdesk_session = cashdesk.active_session
		return timeuntil(cashdesk_session.valid_until)
	except:
		return "-"