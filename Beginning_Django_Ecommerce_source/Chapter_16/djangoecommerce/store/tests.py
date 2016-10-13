from django.test import TestCase, Client
from django.core import urlresolvers

from store.models import Category, Product

import httplib

class StoreTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_get_homepage(self):
        home_url = urlresolvers.reverse('store_home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, httplib.OK)
        
    def test_get_category_page(self):
        category = Category.all().get()
        url = category.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, httplib.OK)
        
    #def NO_test_get_product_page(self):
    #    product = Product.all().get()
    #    url = product.get_absolute_url()
    #    response = self.client.get(url)
    #    self.assertEqual(response.status_code, httplib.OK)
        
        