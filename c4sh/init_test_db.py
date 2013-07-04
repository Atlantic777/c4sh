from django.core.management import setup_environ
import settings, datetime
setup_environ(settings)

from c4sh.backend.models import *
from c4sh.desk.models import *
from c4sh.preorder.models import *
def date(pd):
	return datetime.datetime.strptime(pd, "%Y-%m-%dT%H:%M:%SZ")

t = Ticket(
		name = "Dauerkarte",
		receipt_name = "Dauerkarte Fr-So",
		invoice_name = "Dauerkarte 01.01-03.01",
		description = "Internal <b>HTML-enabled</b> description",
		sale_price = 23.50,
		invoice_price = 23.50,
		currency = "EUR",
		tax_rate = 19,
		rabate_rate = 0,
		limit_timespan = False,
		limit_supervisor = False,
		receipt_autoprint = True,
		receipt_advice = "c4sh dankt.",
		invoice_autoprint = False,
		invoice_advice = "LOL DANKE",
		active = True,
		deleted = False
	).save()

tt = Ticket(
		name = "Tageskarte Fr",
		receipt_name = "Tageskarte Freitag",
		invoice_name = "Tageskarte fuer Freitag, 01.01.",
		description = "Internal <b>HTML-enabled</b> description for Tageskarte",
		sale_price = 11.11,
		invoice_price = 11.11,
		currency = "EUR",
		tax_rate = 19,
		rabate_rate = 0,
		limit_timespan = True,
		valid_from = date("2011-11-20T23:59:00Z"),
		valid_until = date("2011-12-31T00:00:00Z"),
		limit_supervisor = False,
		receipt_autoprint = True,
		receipt_advice = "c4sh dankt.",
		invoice_autoprint = False,
		invoice_advice = "LOL DANKE",
		active = True,
		deleted = False
	).save()

cd = Cashdesk(
		name = "Kasse 1",
		invoice_name = "1",
		ip = "10.0.2.2",
		receipt_printer = False,
		invoice_printer = False,
		active = True,
		allow_supervisor = True
	).save()
