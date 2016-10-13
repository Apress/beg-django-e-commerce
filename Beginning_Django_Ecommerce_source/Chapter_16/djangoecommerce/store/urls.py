from django.conf.urls.defaults import *
#from django.core.urlresolvers import reverse

from brubeck.forms import ProductAddToCartForm

urlpatterns = patterns('store.views',
    (r'^$', 'index', {'template_name':'store_index.html'},'store_home'),
    (r'^category/(?P<category_key>.+)/$', 'show_category', {'template_name': 'store_category.html'}, 'store_category'),
    (r'^product/(?P<product_key>.+)/$', 'show_product', {'template_name': 'store_product.html',
                                                             'form_class': ProductAddToCartForm},
                                                             'store_product'),
)
