from django.conf.urls.defaults import patterns, include, url
from django.contrib import auth
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
	url(r'^login/$', 'login', {'template_name': 'base/login.html'}, name="login"),
	url(r'^logout/$', 'logout', {'next_page': '/'}, name="logout"),
)

urlpatterns += patterns('c4sh.desk.views',
	url(r'^$', 'dashboard_view', name="dashboard"),
	url(r'^sell/$', 'sell_action', name="desk-sell"),
	url(r'^sale/(?P<sale_id>\d+)/$', 'sale_view', name='desk-sale')
)

urlpatterns += patterns('c4sh.backend.views',
	url(r'^backend/$', 'dashboard_view', name="backend-dashboard"),
	url(r'^backend/cashdesks/$', 'cashdesks_view', name="backend-cashdesks"),
	url(r'^backend/sale/(?P<sale_id>\d+)/$', 'sale_detail_view', name="backend-sale-detail"),
	url(r'^fail/', 'static_view', {'template': 'fail.html'}, name="fail"),
)

urlpatterns += patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
   (r'^api/', include('c4sh.api.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        	{'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
	)
	urlpatterns += staticfiles_urlpatterns()
