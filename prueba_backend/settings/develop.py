from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES_LIST = {
    'staging': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbprueba',
        'USER': 'root',
        'HOST': 'mysql',  #<---
        'PORT': '3306',   #<---
        'PASSWORD': 'django*2121',
        'default-character-set': 'utf8',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    # 'sqlite': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

DATABASES = {
    'default': DATABASES_LIST['staging']
}

INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'fw.rest.permissions.AdminPermissions'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'prueba_backend.backends.BackendPagination',
    'DATETIME_FORMAT': "%d/%m/%Y %H:%M:%S",
    'DATE_FORMAT': "%d/%m/%Y",
}
