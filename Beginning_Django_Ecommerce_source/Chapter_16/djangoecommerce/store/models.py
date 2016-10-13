# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

class Category(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    is_active = db.BooleanProperty(default=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ('store_category', (), { 'category_key': self.key()})

    @property
    def products(self):
        return Product.gql('WHERE category = :1', self.key())

class Product(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    is_active = db.BooleanProperty(default=True)
    is_featured = db.BooleanProperty(default=False)
    price = db.FloatProperty()
    
    category = db.ReferenceProperty(Category)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('store_product', (), { 'product_key': self.key()})
    
