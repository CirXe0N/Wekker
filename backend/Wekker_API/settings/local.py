from .base import *

DEBUG = True
ADMIN_ENABLED = True

INSTALLED_APPS += [
    'storages',
]

# CORS

CORS_ORIGIN_ALLOW_ALL = True

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Static settings

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media settings

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000