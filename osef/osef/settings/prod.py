from .base import *

DEBUG = True

ALLOWED_HOSTS = []

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

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
	'fields': 'id,name,email', # needed starting from protocol v2.4
}

SOCIAL_AUTH_FACEBOOK_KEY = '1579555865680294'
SOCIAL_AUTH_FACEBOOK_SECRET = '07b8b7ebf67ee0c72099e4a6fafccb34'