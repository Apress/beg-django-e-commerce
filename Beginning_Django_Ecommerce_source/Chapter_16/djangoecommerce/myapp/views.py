# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
from google.appengine.ext import db
from mimetypes import guess_type
from myapp.forms import PersonForm
from myapp.models import Contract, File, Person
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

def list_people(request):
    return object_list(request, Person.all(), paginate_by=10)

def show_person(request, key):
    return object_detail(request, Person.all(), key)

def add_person(request):
    return create_object(request, form_class=PersonForm,
        post_save_redirect=reverse('myapp.views.show_person',
                                   kwargs=dict(key='%(key)s')))

def edit_person(request, key):
    return update_object(request, object_id=key, form_class=PersonForm)

def delete_person(request, key):
    return delete_object(request, Person, object_id=key,
        post_delete_redirect=reverse('myapp.views.list_people'))

def download_file(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')

def create_admin_user(request):
    user = User.get_by_key_name('admin')
    if not user or user.username != 'admin' or not (user.is_active and
            user.is_staff and user.is_superuser and
            user.check_password('admin')):
        user = User(key_name='admin', username='admin',
            email='admin@localhost', first_name='Boss', last_name='Admin',
            is_active=True, is_staff=True, is_superuser=True)
        user.set_password('admin')
        user.put()
    return render_to_response(request, 'myapp/admin_created.html')
