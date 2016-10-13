from django import template
from django.contrib.flatpages.models import FlatPage
from ecomstore.catalog.models import Category
from ecomstore.cart import cart

from django.core.cache import cache
from ecomstore.settings import CACHE_TIMEOUT

register = template.Library()

@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count }

@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    list_cache_key = 'active_category_link_list'
    active_categories = cache.get(list_cache_key)
    if not active_categories:
        active_categories = Category.active.all()
        cache.set(list_cache_key, active_categories, CACHE_TIMEOUT)
    return {
        'active_categories': active_categories,
        'request_path': request_path
    }

@register.inclusion_tag("tags/footer.html")
def footer_links():
    flatpage_list = FlatPage.objects.all()
    return {'flatpage_list': flatpage_list }

@register.inclusion_tag("tags/product_list.html")
def product_list(products, header_text):
    return { 'products': products,
            'header_text': header_text }
