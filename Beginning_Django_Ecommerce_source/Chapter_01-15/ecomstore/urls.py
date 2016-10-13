from django.conf.urls.defaults import *
from ecomstore import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os

urlpatterns = patterns('',
    # Example:
    # (r'^ecomstore/', include('ecomstore.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^', include('ecomstore.catalog.urls')),
    (r'^cart/', include('cart.urls')),
    (r'^checkout/', include('checkout.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^search/', include('search.urls')),
    (r'^billing/', include('billing.urls')),
    (r'^', include('marketing.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root' : os.path.join(settings.CURRENT_PATH, 'static') }),
)

handler404 = 'ecomstore.views.file_not_found_404'
#handler500 = 'ecomstore.views.server_error_500'
