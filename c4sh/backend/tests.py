import sys
from c4sh.backend import models as bmodels
from c4sh.desk import models as dmodels
from c4sh.preorder import models as pmodels

tickets = pmodels.PreorderTicket.objects.all()

for ticket in tickets:
	print "%s (ID: %d)" % (ticket, ticket.backend_id)

	try:
		bticket = bmodels.Ticket.objects.get(pk=ticket.backend_id)
		print "Backend ticket does already exist.."
	except bmodels.Ticket.DoesNotExist:
		bticket = bmodels.Ticket(
			id = ticket.backend_id,
			name = ticket.name,
			receipt_name = ticket.name,
			invoice_name = ticket.name,
			description = "",
			sale_price = ticket.price,
			invoice_price = ticket.price,
			currency = ticket.currency,
			tax_rate = ticket.tax_rate,
			rabate_rate = 0,
			active = 1
		).save()

		print "No backend ticket found, creating.."

	print "=============="

sys.exit(0)
