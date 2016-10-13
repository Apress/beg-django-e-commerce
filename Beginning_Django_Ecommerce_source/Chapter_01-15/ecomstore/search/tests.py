from django.test import TestCase, Client
from django.core import urlresolvers
from django.utils import html

import httplib

class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        home_url = urlresolvers.reverse('catalog_home')
        response = self.client.get(home_url)
        self.failUnless(response.status_code, httplib.OK)

    def test_html_escaped(self):
        """ search text displayed on results page is HTML-encoded """
        search_term = '<script>alert(xss)</script>'
        search_url = urlresolvers.reverse('search_results')
        search_request = search_url + '?q=' + search_term
        response = self.client.get(search_request)
        self.failUnlessEqual(response.status_code, httplib.OK)
        escaped_term = html.escape(search_term)
        self.assertContains(response, escaped_term)
