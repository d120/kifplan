"""
Django settings for kiffelverwaltung project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "http://localhost:8000/"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$_^yz6o93(#y)p-s(n8skccx*umc$3=y+3h0#mpebc6hva)pij'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',
    'rest_framework',
    'import_export',
    'ajax_select',
    
    'kiffel',
    'eduroam',
    'oplan',
    'frontend',
    'kdvadmin',
    'neuigkeiten',
    
    
    #'debug_toolbar',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'kiffelverwaltung.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kiffelverwaltung.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    )
}


# Auth
AUTH_USER_MODEL = 'kiffel.Person'
LOGIN_URL = 'mysite_login'
LOGOUT_URL = 'mysite_logout'
LOGIN_REDIRECT_URL = 'frontend:index'


# Use KDV tables managed by kifplan/django (True)? Or access existing tables by external KDV App (False)
USE_KIFPLAN_KDV_TABLES = True

#from django.http import HttpResponse
#import json   
#
#MIDDLEWARE_CLASSES += (
#    'kiffelverwaltung.settings.NonHtmlDebugToolbarMiddleware',
#)
#INTERNAL_IPS = ['178.8.206.38']
#
#class NonHtmlDebugToolbarMiddleware(object):
#    """
#    The Django Debug Toolbar usually only works for views that return HTML.
#    This middleware wraps any non-HTML response in HTML if the request
#    has a 'debug' query parameter (e.g. http://localhost/foo?debug)
#    Special handling for json (pretty printing) and
#    binary data (only show data length)
#    """
#
#    @staticmethod
#    def process_response(request, response):
#        if request.GET.get('debug') == '':
#            if response['Content-Type'] == 'application/octet-stream':
#                new_content = '<html><body>Binary Data, ' \
#                    'Length: {}</body></html>'.format(len(response.content))
#                response = HttpResponse(new_content)
#            elif response['Content-Type'] != 'text/html':
#                content = response.content
#                try:
#                    json_ = json.loads(content)
#                    content = json.dumps(json_, sort_keys=True, indent=2)
#                except ValueError:
#                    pass
#                except TypeError:
#                    pass
#                response = HttpResponse('<html><body><pre>{}'
#                                        '</pre></body></html>'.format(content))
#
#        return response



try:
        from kiffelverwaltung.settings_local import *
except ImportError:
        pass


