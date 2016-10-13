from django.test import TestCase, Client
from django.core import urlresolvers
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.views.defaults import page_not_found
from django.db import IntegrityError
from django.utils import html

from ecomstore.catalog.models import Category, Product, ProductReview
from ecomstore.catalog.forms import ProductAddToCartForm

from decimal import Decimal
import httplib

class NewUserTestCase(TestCase):
    """ tests an Anonymous user browing the pages of the site """
    def setUp(self):
        self.client = Client()
        logged_in = self.client.session.has_key(SESSION_KEY)
        self.assertFalse(logged_in)

    def test_view_homepage(self):
        home_url = urlresolvers.reverse('catalog_home')
        response = self.client.get(home_url)
        # check that we did get a response
        self.failUnless(response)
        # check that status code of response was success
        self.assertEqual(response.status_code, httplib.OK)
        
    def test_view_category(self):
        """ test category view loads """
        category = Category.active.all()[0]
        category_url = category.get_absolute_url()
        # get the template_name arg from URL entry
        url_entry = urlresolvers.resolve(category_url)
        template_name = url_entry[2]['template_name']
        # emulate loading of category page
        response = self.client.get(category_url)
        # test that we got a response
        self.failUnless(response)
        # test that the HTTP status code was "OK"
        self.assertEqual(response.status_code, httplib.OK)
        # test that we used the category.html template in response
        self.assertTemplateUsed(response, template_name)
        
    def test_view_product(self):
        """ test product view loads """
        product = Product.active.all()[0]
        product_url = product.get_absolute_url()
        url_entry = urlresolvers.resolve(product_url)
        template_name = url_entry[2]['template_name']
        response = self.client.get(product_url)
        self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, product.name)
        self.assertContains(response, html.escape(product.description))
        # check for cart form in product page response
        cart_form = response.context[0]['form']
        self.failUnless(cart_form)
        # check that the cart form is instance of correct form class
        self.failUnless(isinstance(cart_form, ProductAddToCartForm))
        
        product_reviews = response.context[0].get('product_reviews',None)
        self.failIfEqual(product_reviews, None)
        
        
class ActiveProductManagerTestCase(TestCase):
    """ tests that Product.active manager class returns only active products, and that
    inactive products return the 404 Not Found template 
    """
    def setUp(self):
        self.client = Client()
        logged_in = self.client.session.has_key(SESSION_KEY)
        self.assertFalse(logged_in)

    def test_inactive_product_returns_404(self):
        """ test that inactive product returns a 404 error """
        inactive_product = Product.objects.filter(is_active=False)[0]
        inactive_product_url = inactive_product.get_absolute_url()
        # load the template file used to render the product page
        url_entry = urlresolvers.resolve(inactive_product_url)
        template_name = url_entry[2]['template_name']
        # load the name of the default django 404 template file
        django_404_template = page_not_found.func_defaults[0]
        response = self.client.get(inactive_product_url)
        self.assertTemplateUsed(response, django_404_template)
        self.assertTemplateNotUsed(response, template_name)


class CategoryTestCase(TestCase):
    """ tests the methods on the catalog.Category model class """
    def setUp(self):
        self.category = Category.active.all()[0]
        self.client = Client()

    def test_permalink(self):
        url = self.category.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.failUnlessEqual(response.status_code, httplib.OK)

    def test_unicode(self):
        self.assertEqual(self.category.__unicode__(), self.category.name)


class ProductTestCase(TestCase):
    """  tests the methods and custom properties on the catalog.Product model class """
    def setUp(self):
        self.product = Product.active.all()[0]
        self.product.price = Decimal('199.99')
        self.product.save()
        self.client = Client()

    def test_sale_price(self):
        """ if price is greater than old_price, sale_price = price """
        self.product.old_price = Decimal('220.00')
        self.product.save()
        self.failIfEqual(self.product.sale_price, None)
        self.assertEqual(self.product.sale_price, self.product.price)
        
    def test_no_sale_price(self):
        """ if old_price is less than price, sale_price returns None """
        self.product.old_price = Decimal('0.00')    
        self.product.save()
        self.failUnlessEqual(self.product.sale_price, None)

    def test_permalink(self):
        url = self.product.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)

    def test_unicode(self):
        self.assertEqual(self.product.__unicode__(), self.product.name)


class ProductReviewTestCase(TestCase):
    """ tests the catalog.ProductReview model class """
    def test_orphaned_product_review(self):
        """ attempt to save ProductReview instance with no product raises IntegrityError """
        pr = ProductReview()
        self.assertRaises(IntegrityError, pr.save)
        
    def test_product_review_defaults(self):
        """ attempt to save ProductReview instance with fields empty resorts to class defaults """
        user = User.objects.all()[0]
        product = Product.active.all()[0]
        pr = ProductReview(user=user, product=product)
        pr.save()
        for field in pr._meta.fields:
                if field.has_default():
                    self.assertEqual(pr.__dict__[field.name], field.default)
                
