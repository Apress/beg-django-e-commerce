# Django settings for ecomstore project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

SITE_NAME = 'Modern Musician'
META_KEYWORDS = 'Music, instruments, sheet music, musician'
META_DESCRIPTION = 'Modern Musician is an online supplier of instruments, sheet music, and other accessories for musicians'

# CURRENT_PATH = os.path.abspath('.').decode('utf-8').replace('\\','/')
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))

# Upon deployment, change to True
ENABLE_SSL = False

# Uncomment the following line after you have installed memcached on your local development machine
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

CACHE_TIMEOUT = 60 * 60


PRODUCTS_PER_PAGE = 1
PRODUCTS_PER_ROW = 4

LOGIN_REDIRECT_URL = '/accounts/my_account/'

SESSION_COOKIE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS 

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(CURRENT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'ecomstore.utils.context_processors.ecomstore',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'djangodblog.DBLogMiddleware',
    'ecomstore.marketing.urlcanon.URLCanonicalizationMiddleware',
    'ecomstore.SSLMiddleware.SSLRedirect',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

AUTH_PROFILE_MODULE = 'accounts.userprofile'

ROOT_URLCONF = 'ecomstore.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(CURRENT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'ecomstore.catalog',
    'ecomstore.cart',
    'ecomstore.accounts',
    'ecomstore.search',
    'ecomstore.checkout',
    'ecomstore.utils',
    'ecomstore.stats',
    'djangodblog',
    'tagging',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'ecomstore.billing',
    'ecomstore.caching',
)
# for use with URL Canonicalization Middleware:
# this is the canonical hostname to be used by your app (required)
CANON_URL_HOST = 'www.your-domain.com'
# these are the hostnames that will be redirected to the CANON_URL_HOSTNAME 
# (optional; if not provided, all non-matching will be redirected)
CANON_URLS_TO_REWRITE = ['your-domain.com', 'other-domain.com']

# Google Checkout API credentials
GOOGLE_CHECKOUT_MERCHANT_ID = ''
GOOGLE_CHECKOUT_MERCHANT_KEY = ''
GOOGLE_CHECKOUT_URL = 'https://sandbox.google.com/checkout/api/checkout/v2/merchantCheckout/Merchant/' + GOOGLE_CHECKOUT_MERCHANT_ID

# Authorize.Net API Credentials
AUTHNET_POST_URL = 'test.authorize.net'
AUTHNET_POST_PATH = '/gateway/transact.dll'
AUTHNET_LOGIN = ''
AUTHNET_KEY = ''

# Google Analytics tracking ID
# should take the form of 'UA-xxxxxxx-x', where the X's are digits
ANALYTICS_TRACKING_ID = ''

try:
    from settings_local import *
except ImportError:
    pass
