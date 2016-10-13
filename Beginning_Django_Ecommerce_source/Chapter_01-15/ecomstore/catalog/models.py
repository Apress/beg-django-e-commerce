from django.db import models
from django.http import Http404
from ecomstore import settings
from django.contrib.auth.models import User
import tagging

from django.db.models.signals import post_save, post_delete
from ecomstore.caching.caching import cache_update, cache_evict

class ActiveCategoryManager(models.Manager):
    """ Manager class to return only those categories where each instance is active """
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)

class Category(models.Model):
    """ model class containing information about a category in the product catalog """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    active = ActiveCategoryManager()

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('catalog_category', (), { 'category_slug': self.slug })
    
    @property
    def cache_key(self):
        return self.get_absolute_url()
    

class ActiveProductManager(models.Manager):
    """ Manager class to return only those products where each instance is active """
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)
    
class FeaturedProductManager(models.Manager):
    """ Manager class to return only those products where each instance is featured """
    def get_query_set(self):
        return super(FeaturedProductManager, self).get_query_set().filter(is_active=True).filter(is_featured=True)

class Product(models.Model):
    """ model class containing information about a product; instances of this class are what the user
    adds to their shopping cart and can subsequently purchase
    
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    brand = models.CharField(max_length=50) 
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,
                                    blank=True,default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords",max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    
    # image fields, added in Chapter 7
    # image fields require a varchar(100) in db
    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=200)
    
    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), { 'product_slug': self.slug })
    
    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
    
    def cross_sells(self):
        """ gets other Product instances that have been combined with the current instance in past orders. Includes the orders
        that have been placed by anonymous users that haven't registered
        """
        from ecomstore.checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        products = Product.active.filter(orderitem__in=order_items).distinct()
        return products
    
    # users who purchased this product also bought....
    def cross_sells_user(self):
        """ gets other Product instances that have been ordered by other registered customers who also ordered the current
        instance. Uses all past orders of each registered customer and not just the order in which the current 
        instance was purchased
        
        """
        from ecomstore.checkout.models import Order, OrderItem
        from django.contrib.auth.models import User
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products
    
    def cross_sells_hybrid(self):
        """ gets other Product instances that have been both been combined with the current instance in orders placed by 
        unregistered customers, and all products that have ever been ordered by registered customers
        
        """
        from ecomstore.checkout.models import Order, OrderItem
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter( Q(order__in=orders) | 
                      Q(order__user__in=users) 
                      ).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products
    
    @property
    def cache_key(self):
        return self.get_absolute_url()
try:
    tagging.register(Product)
except tagging.AlreadyRegistered:
    pass
    
class ActiveProductReviewManager(models.Manager):
    """ Manager class to return only those product reviews where each instance is approved """
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)
        
class ProductReview(models.Model):
    """ model class containing product review data associated with a product instance """
    RATINGS = ((5,5),(4,4),(3,3),(2,2),(1,1),)
    
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()
    
    objects = models.Manager()
    approved = ActiveProductReviewManager()
    
# attach signals to Product and Category model classes 
# to update cache data on save and delete operations
post_save.connect(cache_update, sender=Product)
post_delete.connect(cache_evict, sender=Product) 
post_save.connect(cache_update, sender=Category)
post_delete.connect(cache_evict, sender=Category)
