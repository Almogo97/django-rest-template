from .base import *  # noqa

INSTALLED_APPS += ['django_extensions']

# Included to pass the tests
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)


MIDDLEWARE += (
    'qinspect.middleware.QueryInspectMiddleware',
)

QUERY_INSPECT_ENABLED = True

LOGGING = {
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
