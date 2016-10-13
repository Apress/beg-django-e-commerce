from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from brubeck.models import CartItem
from brubeck.forms import ProductAddToCartForm
from brubeck import cart

def show_cart(request, template_name='brubeck_cart.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        submit = postdata.get('submit','')
        item_key = postdata.get('cart_item_id')
        if postdata.get('submit','') == 'Update':
            quantity = postdata.get('quantity', 1)
            cart.update_item(item_key, quantity)
        if postdata.get('submit','') == 'Remove':
            cart.remove_item(item_key)
    shopping_cart = cart.get(request)
    page_title = u'Shopping Cart'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))