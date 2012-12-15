from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view

from c4sh.api.handlers import *

PreorderPosition = Resource(handler=PreorderPositionHandler)
PreorderPositionSearch = Resource(handler=PreorderPositionSearchHandler)
HonoraryMemberNumberSearch = Resource(handler=HonoraryMemberNumberSearchHandler)
OpenCashDrawer = Resource(handler=OpenCashDrawerHandler)
ReprintReceipt = Resource(handler=ReprintReceiptHandler)

urlpatterns = patterns('',
	url(r'^preorder_position/(?P<uuid>([a-fA-F0-9\-])+)/$', PreorderPosition),
	url(r'^preorder_position_search/(?P<uuid>([a-fA-F0-9\-])+)/$', PreorderPositionSearch),
	url(r'^honoary_member_number_search/(?P<number>([\w ])+)/$', HonoraryMemberNumberSearch),
	url(r'^cashdrawer/open/(?P<cashdesk_id>\d+)/$', OpenCashDrawer),
	url(r'^receipt/print/(?P<sale_id>\d+)/$', ReprintReceipt),
	url(r'^receipt/print/(?P<sale_id>\d+)/(?P<cashdesk_id>\d+)/$', ReprintReceipt),

	url(r'^$', documentation_view)
)