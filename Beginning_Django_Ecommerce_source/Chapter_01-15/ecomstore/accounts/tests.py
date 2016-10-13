from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core import urlresolvers

from ecomstore.catalog.models import Product
from ecomstore.checkout.models import Order, OrderItem
from ecomstore import settings

import httplib

TEST_USERNAME = "alice"
TEST_PASSWORD = "test"

class OrderHistoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        logged_in = self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        self.failUnless(logged_in)
        self.user = User.objects.get(username=TEST_USERNAME)
        self.failUnless(self.user)
        
    def test_browse_order_history(self):
        """ customer can view the details of their own past orders """
        my_account_url = urlresolvers.reverse('my_account')
        response = self.client.get(my_account_url)
        self.failUnlessEqual(response.status_code, httplib.OK)
        order = Order.objects.filter(user=self.user)[0]
        self.assertContains(response, unicode(order))
        
        order_url = order.get_absolute_url()
        response = self.client.get(order_url)
        self.failUnlessEqual(response.status_code, httplib.OK)
        products = Product.objects.filter(orderitem__order=order)
        for p in products:
            self.assertContains(response, unicode(p))
            
class LoginTestCase(TestCase):
    """ test customer login """
    def setUp(self):
        self.client = Client()
        self.login_url = urlresolvers.reverse('login')
        self.login_data = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
        
    def test_user_login(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        
    def test_user_login_redirect(self):
        """ if URL contains 'next' parameter, customer is redirected after successfully logging in """
        my_account_url = urlresolvers.reverse('my_account')
        redirect_url = self.login_url + '?next=' + my_account_url
        
        response = self.client.get(my_account_url)
        self.assertRedirects(response, redirect_url, 
                             status_code=httplib.FOUND, target_status_code=httplib.OK)
        
        response = self.client.post(redirect_url, self.login_data)
        self.assertRedirects(response, my_account_url, 
                             status_code=httplib.FOUND, target_status_code=httplib.OK)
        
class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = urlresolvers.reverse('register')
        
    def test_user_registration(self):
        pass
        
