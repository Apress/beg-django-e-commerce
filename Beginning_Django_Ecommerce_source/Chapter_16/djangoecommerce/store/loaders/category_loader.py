import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
from djangoecommerce.store.models import Category

class CategoryLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Category',
                               [('name', unicode),
                                ('slug', unicode),
                                ('description', db.Text),
                                ('is_active', bool)
                               ])

loaders = [CategoryLoader]