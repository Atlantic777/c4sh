from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view

from c4sh.api.handlers import *

PreorderPosition = Resource(handler=PreorderPositionHandler)
PreorderPositionSearch = Resource(handler=PreorderPositionSearchHandler)

urlpatterns = patterns('',
	url(r'^preorder_position/(?P<uuid>([a-fA-F0-9\-])+)/$', PreorderPosition),
	url(r'^preorder_position_search/(?P<uuid>([a-fA-F0-9\-])+)/$', PreorderPositionSearch),
	url(r'^$', documentation_view)
)