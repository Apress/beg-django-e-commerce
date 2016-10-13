from ecomstore.checkout import google_checkout
from ecomstore.cart import cart
from ecomstore.checkout.models import Order, OrderItem
from ecomstore.checkout.forms import CheckoutForm
from ecomstore.checkout import authnet
from ecomstore import settings

from django.core import urlresolvers
import urllib

def get_checkout_url(request):
    """ returns the URL from the checkout module for cart """
    # use this for Google Checkout API:
    # return google_checkout.get_checkout_url(request)
    
    # use this for our own-site checkout
    return urlresolvers.reverse('checkout')
    
def process(request):
    """ takes a POST request containing valid order data; pings the payment gateway with the billing 
    information and returns a Python dictionary with two entries: 'order_number' and 'message' based on
    the success of the payment processing. An unsuccessful billing will have an order_number of 0 and an error message, 
    and a successful billing with have an order number and an empty string message.
    
    """
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    
    postdata = request.POST.copy()
    card_num = postdata.get('credit_card_number','')
    exp_month = postdata.get('credit_card_expire_month','')
    exp_year = postdata.get('credit_card_expire_year','')
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv','')
    amount = cart.cart_subtotal(request)
    
    results = {}
    
    response = authnet.do_auth_capture(amount=amount, 
                                       card_num=card_num, 
                                       exp_date=exp_date,
                                       card_cvv=cvv)
    if response[0] == APPROVED:
        transaction_id = response[6]
        order = create_order(request, transaction_id)
        results = {'order_number': order.id, 'message': u''}
    if response[0] == DECLINED:
        results = {'order_number': 0, 'message': u'There is a problem with your credit card.'}
    if response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {'order_number': 0, 'message': u'Error processing your order.'}
    return results

def create_order(request, transaction_id):
    """ if the POST to the payment gateway successfully billed the customer, create a new order
    containing each CartItem instance, save the order with the transaction ID from the gateway,
    and empty the shopping cart
    
    """
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    
    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = None
    if request.user.is_authenticated():
        order.user = request.user
    order.status = Order.SUBMITTED
    order.save()
    
    if order.pk:
        """ if the order save succeeded """
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            """ create order item for each cart item """
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price  # now using @property
            oi.product = ci.product
            oi.save()
        # all set, clear the cart
        cart.empty_cart(request)
        
        # save profile info for future orders
        if request.user.is_authenticated():
            from ecomstore.accounts import profile
            profile.set(request)
        
    return order
