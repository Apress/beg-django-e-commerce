from django.db import models
from ecomstore.catalog.models import Product

class CartItem(models.Model):
    """ model class containing information each Product instance in the customer's shopping cart """
    cart_id = models.CharField(max_length=50, db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False)
            
    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']
    
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
    
    def augment_quantity(self, quantity):
        """ called when a POST request comes in for a Product instance already in the shopping cart """
        self.quantity = self.quantity + int(quantity)
        self.save()