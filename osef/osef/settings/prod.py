from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'osef',
        'USER': 'osef',
        'PASSWORD': 'osef',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child('static')
MEDIA_URL = '/media/'

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
	'fields': 'id,name,email', # needed starting from protocol v2.4
}

SOCIAL_AUTH_FACEBOOK_KEY = '211512812606854'
SOCIAL_AUTH_FACEBOOK_SECRET = '905ed0e6c3b38e6c8ce7fb0304c95616'