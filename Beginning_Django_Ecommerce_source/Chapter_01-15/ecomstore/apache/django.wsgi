import os, sys

wsgi_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.dirname(wsgi_dir)
sys.path.append(project_dir)
project_settings = os.path.join(project_dir,'settings')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecomstore.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
