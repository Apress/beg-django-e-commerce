from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.views',
    (r'^$', 'show_cart', {'template_name':'brubeck_cart.html'}, 'show_cart'),
)
