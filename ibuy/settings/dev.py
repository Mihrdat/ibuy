from .common import *
import config

SECRET_KEY = 'django-insecure-d7^4g)&m(*4to2b^bbczvk5v5mzawl%7_0@+su3hc2*s2#go(r'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ibuy',
        'HOST': config.DB_HOST,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASSWORD,
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
}
