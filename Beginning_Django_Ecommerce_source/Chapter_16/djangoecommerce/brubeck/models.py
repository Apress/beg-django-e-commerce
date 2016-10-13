# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

from store.models import Product

class CartItem(db.Model):
    quantity = db.IntegerProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)
    cart_id = db.StringProperty()
    product = db.ReferenceProperty(Product,
                                   collection_name='products')
    
    @property
    def total(self):
        return self.quantity * self.product.price

    @property
    def name(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()
