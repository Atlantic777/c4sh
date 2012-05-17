from piston.handler import BaseHandler
from piston.utils import *
from c4sh.backend import models as bmodels
from c4sh.desk import models as dmodels
from c4sh.preorder import models as pmodels

from c4sh.desk.tools import open_drawer

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

class OpenCashDrawerHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request):
		open_drawer()
		return rc.ALL_OK