from django import template
from google.appengine.ext import db
from store.models import Category

register = template.Library()

@register.inclusion_tag("store_category_list.html")
def category_list():
    query = db.Query(Category)
    query.filter('is_active = ', True)
    query.order('name')
    categories = query.fetch(20)
    return {'categories': categories }