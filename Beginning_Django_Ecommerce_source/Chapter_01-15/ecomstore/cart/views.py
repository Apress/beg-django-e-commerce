from django.shortcuts import render_to_response, get_object_or_404
from ecomstore.cart import cart
from django.template import RequestContext

from django.http import HttpResponseRedirect
from ecomstore.checkout import checkout
from ecomstore import settings

def show_cart(request, template_name="cart/cart.html"):
    """ view function for the page displaying the customer shopping cart, and allows for the updating of quantities
    and removal product instances 
    
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    # need for Google Checkout button
    merchant_id = settings.GOOGLE_CHECKOUT_MERCHANT_ID
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
