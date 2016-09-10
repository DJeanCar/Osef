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
MEDIA_URL = '/media/'

SOCIAL_AUTH_FACEBOOK_KEY = '742694022439888'
SOCIAL_AUTH_FACEBOOK_SECRET = '5450a69e21f912864b7e95a785a14515'