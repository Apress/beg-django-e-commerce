from ecomstore.search.models import SearchTerm
from ecomstore.catalog.models import Product
from django.db.models import Q

from ecomstore.stats import stats

STRIP_WORDS = ['a','an','and','by','for','from','in','no','not',
               'of','on','or','that','the','to','with']

def store(request, q):
    """ stores the search text """
    # if search term is at least three chars long, store in db
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated():
            term.user = request.user
        term.save()
    
def products(search_text):
    """ get products matching the search text """
    words = _prepare_words(search_text)
    products = Product.active.all()
    results = {}
    for word in words:
        products = products.filter(Q(name__icontains=word) |
        Q(description__icontains=word) |
        Q(sku__iexact=word) |
        Q(brand__icontains=word) |
        Q(meta_description__icontains=word) |
        Q(meta_keywords__icontains=word))
        results['products'] = products
    return results
    
def _prepare_words(search_text):
    """ strip out common words, limit to 5 words """
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]

