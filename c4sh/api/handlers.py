from piston.handler import BaseHandler
from piston.utils import *
from c4sh.backend import models as bmodels
from c4sh.desk import models as dmodels
from c4sh.preorder import models as pmodels
from django.db.models import Q

from c4sh.desk.tools import open_drawer, print_receipt
from c4sh.desk.templatetags.cashdesk_session import cashdesk_session

class SessionTimeLeftHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request):
		return cashdesk_session(request.session)


class PreorderPositionHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = pmodels.PreorderPosition

	def read(self, request, uuid):
		try:
			preorder_position = pmodels.PreorderPosition.objects.get(uuid=uuid)

			if preorder_position.redeemed == True:
				return rc.FORBIDDEN

			return preorder_position.ticket.backend_id
		except pmodels.PreorderPosition.DoesNotExist:
			return rc.NOT_HERE

class PreorderPositionSearchHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = pmodels.PreorderPosition

	def read(self, request, uuid):
		try:
			preorder_positions = pmodels.PreorderPosition.objects.filter(uuid__icontains=uuid, ticket__backend_id__in=bmodels.Ticket.objects.all()).values('ticket__backend_id', 'uuid')[:10]
			return preorder_positions
		except pmodels.PreorderPosition.DoesNotExist:
			return []

class HonoraryMemberNumberSearchHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = bmodels.HonoraryMember

	def read(self, request, number):
		try:
			members = bmodels.HonoraryMember.objects.filter((Q(membership_number__icontains=number) | Q(full_name__icontains=number)) & Q(saleposition=None)).values('membership_number', 'full_name')[:10]
			return members
		except bmodels.HonoraryMember.DoesNotExist:
			return []

class ReprintReceiptHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request, sale_id, cashdesk_id=None):

		sale = dmodels.Sale.objects.get(pk=sale_id)

		if cashdesk_id:
			cashdesk = bmodels.Cashdesk.objects.get(pk=cashdesk_id)
			if not cashdesk.receipt_printer:
				return rc.NOT_HERE
			printer = cashdesk.receipt_printer_name
		else:
			printer = sale.cashdesk.receipt_printer_name

		print_receipt(sale, printer, False)

		return rc.ALL_OK

class OpenCashDrawerHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request, cashdesk_id):

		cashdesk = bmodels.Cashdesk.objects.get(pk=cashdesk_id)
		if not cashdesk.receipt_printer:
			return rc.NOT_HERE

		open_drawer(cashdesk.receipt_printer_name)
		return rc.ALL_OK
