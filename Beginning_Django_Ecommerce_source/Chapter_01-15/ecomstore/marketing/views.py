from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from ecomstore.settings import CURRENT_PATH
from ecomstore.catalog.models import Product
import os

ROBOTS_PATH = os.path.join(CURRENT_PATH, 'marketing/robots.txt')

def robots(request):
    """ view for robots.txt file """
    return HttpResponse(open(ROBOTS_PATH).read(), 'text/plain')

def google_base(request):
    """ view for Google Base Product feed template; returns XML response """
    products = Product.active.all()
    template = get_template("marketing/google_base.xml")
    xml = template.render(Context(locals()))
    return HttpResponse(xml, mimetype="text/xml")