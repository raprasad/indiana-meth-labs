"""Development settings and globals."""

from __future__ import absolute_import

from os.path import join, normpath, dirname
import os
from .base import *

TEST_SETUP_DIR = normpath(join(dirname(dirname(DJANGO_ROOT)), 'test_setup'))
if not isdir(TEST_SETUP_DIR):
    os.makedirs(TEST_SETUP_DIR)

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
#DEBUG = False
#ALLOWED_HOSTS = ('127.0.0.1', 'netdna.bootstrapcdn.com')
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

########## CONFIGURATION FROM JSON FILE

json_secrets_fname = join( dirname(abspath(__file__)), "secret_settings_local.json")
if not isfile(json_secrets_fname):
    raise ValueError('JSON file in settings does not exist: %s' % json_secrets_fname)
try:
    JSON_SECRETS = json.loads(open(json_secrets_fname, 'r').read())
except:
    raise Exception("Failed to parse JSON file for settings: %s" % json_secrets_fname)

########## END CONFIGURATION FROM JSON FILE

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = JSON_SECRETS['EMAIL_SETTINGS']['EMAIL_HOST']

EMAIL_HOST_PASSWORD = JSON_SECRETS['EMAIL_SETTINGS']['EMAIL_HOST_PASSWORD']

EMAIL_HOST_USER = JSON_SECRETS['EMAIL_SETTINGS']['EMAIL_HOST_USER']

EMAIL_PORT = JSON_SECRETS['EMAIL_SETTINGS']['EMAIL_PORT']

EMAIL_USE_TLS = JSON_SECRETS['EMAIL_SETTINGS']['EMAIL_USE_TLS']


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(TEST_SETUP_DIR, 'methlabs.db3')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
   
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    'debug_toolbar',
    'django.contrib.admindocs',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION
