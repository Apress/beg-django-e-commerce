# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from myapp.forms import UserRegistrationForm
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
    ('^admin/(.*)', admin.site.root),
    (r'^', include('store.urls')),
    (r'^cart/', include('brubeck.urls')),
    # Override the default registration form
    url(r'^account/register/$', 'registration.views.register',
        kwargs={'form_class': UserRegistrationForm},
        name='registration_register'),
) + urlpatterns
