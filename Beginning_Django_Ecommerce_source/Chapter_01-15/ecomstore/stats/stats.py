from ecomstore.search.models import SearchTerm
from ecomstore.catalog.models import Product
from ecomstore.stats.models import ProductView
from ecomstore.settings import PRODUCTS_PER_ROW

import os
import base64

def tracking_id(request):
    """ unique ID to determine what pages a customer has viewed """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']
    
def recommended_from_search(request):
    """ get the common words from the stored searches """
    common_words = frequent_search_words(request)
    from ecomstore.search import search
    matching = []
    for word in common_words:
        results = search.products(word).get('products',[])
        for r in results:
            if len(matching) < PRODUCTS_PER_ROW and not r in matching:
                matching.append(r)
    return matching
        
def frequent_search_words(request):
    """ gets the three most common search words from the last 10 searches the current customer has entered """
    # get the ten most recent searches from the database.
    searches = SearchTerm.objects.filter(tracking_id=tracking_id(request)).values('q').order_by('-search_date')[0:10]
    # join all of the searches together into a single string.
    search_string = ' '.join([search['q'] for search in searches])
    # return the top three most common words in the searches
    return sort_words_by_frequency(search_string)[0:3]

def sort_words_by_frequency(some_string):
    """ takes a single string of space-delimited word and returns a list of words they contain from most to least frequent """
    # convert the string to a python list
    words = some_string.split()
    # assign a rank to each word based on frequency
    ranked_words = [[word, words.count(word)] for word in set(words)]
    # sort the words based on descending frequency
    sorted_words = sorted(ranked_words, key = lambda word: -word[1])
    # return the list of words, most frequent first
    return [p[0] for p in sorted_words]

def log_product_view(request, product):
    """ log the current customer as having viewed the given product instance """
    t_id = tracking_id(request)
    try:
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        v.ip_address = request.META.get('REMOTE_ADDR')
        if not request.META.get('REMOTE_ADDR'):
            v.ip_address = '127.0.0.1'
        v.user = None
        v.tracking_id = t_id
        if request.user.is_authenticated():
            v.user = request.user
        v.save()

def recommended_from_views(request):
    """ get product recommendations based on products that the customer has viewed;
    gets list of tracking IDs of other customers who have viewed the products in the current customer's 
    viewed products, and gets products that these other customers also viewed.
    
    """
    t_id = tracking_id(request)
    # get recently viewed products
    viewed = get_recently_viewed(request)
    # if there are previously viewed products, get other tracking ids that have
    # viewed those products also
    if viewed:
        productviews = ProductView.objects.filter(product__in=viewed).values('tracking_id')
        t_ids = [v['tracking_id'] for v in productviews]
        # if there are other tracking ids, get the products that those other customers viewed.
        if t_ids:
            all_viewed = Product.active.filter(productview__tracking_id__in=t_ids)
            # if there are other products, get them, excluding the products that the customer 
            # has already viewed.
            if all_viewed:
                other_viewed = ProductView.objects.filter(product__in=all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    return Product.active.filter(productview__in=other_viewed).distinct()
                
def get_recently_viewed(request):
    """ get settings.PRODUCTS_PER_ROW most recently viewed products for current customer """
    t_id = tracking_id(request)
    views = ProductView.objects.filter(tracking_id=t_id).values('product_id').order_by('-date')[0:PRODUCTS_PER_ROW]
    product_ids = [v['product_id'] for v in views]
    return Product.active.filter(id__in=product_ids)
    