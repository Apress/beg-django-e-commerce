from django.conf.urls.defaults import *

rootpatterns = patterns('',
    (r'^account/', include('registration.urls')),
)
