from django.conf.urls.defaults import *

urlpatterns = patterns('ecomstore.billing.views',
    (r'^add_card/$', 'add_card'),
)