from django.core.cache import cache
from ecomstore.settings import CACHE_TIMEOUT

def cache_update(sender, **kwargs):
    """ signal for updating a model instance in the cache; any Model class using this signal must
    have a uniquely identifying 'cache_key' property. 
    
    """
    item = kwargs.get('instance')
    cache.set(item.cache_key, item, CACHE_TIMEOUT)
    
def cache_evict(sender, **kwargs):
    """ signal for updating a model instance in the cache; any Model class using this signal must
    have a uniquely identifying 'cache_key' property. 
    
    """
    item = kwargs.get('instance')
    cache.delete(item.cache_key)

