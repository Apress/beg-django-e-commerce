from django.db import models
from django import forms
from django.contrib.auth.models import User
from ecomstore.catalog.models import Product
import decimal

class BaseOrderInfo(models.Model):
    """ base class for storing customer order information """
    class Meta:
        abstract = True
        
    #contact info
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    
    #shipping information
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=2)
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)
    
    #billing information
    billing_name = models.CharField(max_length=50)
    billing_address_1 = models.CharField(max_length=50)
    billing_address_2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=2)
    billing_country = models.CharField(max_length=50)
    billing_zip = models.CharField(max_length=10)

class Order(BaseOrderInfo):
    """ model class for storing a customer order instance """
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Submitted'),
                      (PROCESSED,'Processed'),
                      (SHIPPED,'Shipped'),
                      (CANCELLED,'Cancelled'),)
    #order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    transaction_id = models.CharField(max_length=20)
    
    # MOVED INTO PARENT BaseOrderInfo CLASS IN Chapter 6
    #contact info
    #email = models.EmailField(max_length=50)
    #phone = models.CharField(max_length=20)
    
    #shipping information
    #shipping_name = models.CharField(max_length=50)
    #shipping_address_1 = models.CharField(max_length=50)
    #shipping_address_2 = models.CharField(max_length=50, blank=True)
    #shipping_city = models.CharField(max_length=50)
    #shipping_state = models.CharField(max_length=2)
    #shipping_country = models.CharField(max_length=50)
    #shipping_zip = models.CharField(max_length=10)
    
    #billing information
    #billing_name = models.CharField(max_length=50)
    #billing_address_1 = models.CharField(max_length=50)
    #billing_address_2 = models.CharField(max_length=50, blank=True)
    #billing_city = models.CharField(max_length=50)
    #billing_state = models.CharField(max_length=2)
    #billing_country = models.CharField(max_length=50)
    #billing_zip = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u'Order #' + str(self.id)
    
    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total
    
    @models.permalink
    def get_absolute_url(self):
        return ('order_details', (), { 'order_id': self.id })
    
class OrderItem(models.Model):
    """ model class for storing each Product instance purchased in each order """
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    order = models.ForeignKey(Order)
    
    @property
    def total(self):
        return self.quantity * self.price
    
    @property
    def name(self):
        return self.product.name
    
    @property
    def sku(self):
        return self.product.sku
    
    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
    