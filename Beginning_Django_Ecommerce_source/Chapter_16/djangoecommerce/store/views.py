from django.shortcuts import render_to_response
from django.template import RequestContext
from google.appengine.ext import db
from django.core import urlresolvers
from django.http import HttpResponseRedirect, Http404

from store.models import Category, Product
from brubeck.forms import ProductAddToCartForm
from brubeck import cart

def index(request, 
          template_name='store_index.html'):
    page_title = 'Welcome'
    query = db.Query(Product)
    query.filter("is_featured =", True)
    query.filter("is_active =", True)
    featured_products = query.fetch(20)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_category(request, category_key, 
                  template_name="store_category.html"):
    key = db.Key(category_key)
    query = Category.gql('WHERE __key__ = :1 AND is_active = True', key)
    category = query.get()
    if not category:
        raise Http404('Category not found!')
    products = category.products
    page_title = category.name
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def show_product(request, product_key, 
                 template_name="store_product.html",
                 form_class=ProductAddToCartForm):
    key = db.Key(product_key)
    query = Product.gql('WHERE __key__ = :1 AND is_active = True', key)
    product = query.get()
    if not product:
        raise Http404('Product not found!')
    page_title = product.name
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = form_class(postdata)
        if form.is_valid():
            cart.add(request, product_key)
            redirect_url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(redirect_url)
    else:
        form = form_class()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
