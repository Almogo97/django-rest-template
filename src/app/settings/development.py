from .base import *  # noqa

INSTALLED_APPS += ['django_extensions']

MIDDLEWARE += ('qinspect.middleware.QueryInspectMiddleware',)

QUERY_INSPECT_ENABLED = True

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'qinspect': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
