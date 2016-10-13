from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from ecomstore.search import search
from ecomstore import settings

from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from ecomstore.catalog.models import Product

def results(request, template_name="search/results.html"):
    """ template for displaying settings.PRODUCTS_PER_PAGE paginated product results """
    # get current search phrase
    q = request.GET.get('q', '')
    # get current page number. Set to 1 is missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
        
    matching = search.products(q).get('products', [])
    # generate the pagintor object
    paginator = Paginator(matching, 
                          settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
        
    search.store(request, q)
    
    page_title = 'Search Results for: ' + q
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
