from google.appengine.ext import db
from brubeck.models import CartItem
from store.models import Product
from decimal import Decimal

import base64
import os

CART_ID_SESSION_KEY = 'cart_id'

def get_cart_id(request):
    cart_id = request.session.get(CART_ID_SESSION_KEY, '')
    if not cart_id:
        cart_id = _generate_cart_id()
        request.session[CART_ID_SESSION_KEY] = cart_id
    return cart_id
        
def _generate_cart_id():
    return base64.b64encode(os.urandom(36))

def add(request, product_key):
    postdata = request.POST.copy()
    quantity = int(postdata.get('quantity', 1))
    product = Product.get(product_key)
    item = CartItem.all().filter('product = ', product).filter('cart_id = ', get_cart_id(request)).get()
    if not item:
        item = CartItem()
        item.product = product
        item.quantity = quantity
        item.cart_id = get_cart_id(request)
        item.put()
    else:
        item.quantity = item.quantity + quantity
        item.put()
    
class Cart(object):
    def __init__(self, request):
        cart_id = get_cart_id(request)
        query = CartItem.all().filter('cart_id = ', cart_id)
        self.items = query.fetch(20)
        self.subtotal = Decimal('0.00')
        for item in self.items:
            self.subtotal += Decimal(str(item.total))
                
def get(request):
    return Cart(request)

def update_item(item_key, quantity):
    key = db.Key(item_key)
    item = CartItem.get(key)
    if item:
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = int(quantity)
            item.put()

def remove_item(item_key):
    key = db.Key(item_key)
    item = CartItem.get(key)
    if item:
        item.delete()



