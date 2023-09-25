"""
Django settings for oasis project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# local start
SECRET_KEY = 'django-insecure-zu8d8l(@0^chw%mh^02o5pijhjgvcg&3i-nuwp(k-f+_tds7$n=30=(==(_Wrong_skey))'
# local end

# production start
#SECRET_KEY = os.getenv('SECRET_KEY')
# production end

# SECURITY WARNING: don't run with debug turned on in production!

# local start
DEBUG = True
# local end

# production start
#DEBUG = os.getenv('DEBUG')
# production end

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'account',
    'octoparse',
    'pyscrap',
    'pyazure',
    
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_crontab',
    'django_celery_results',
    'django_celery_beat',
         


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oasis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'oasis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# local start
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
# local end


# Driver={ODBC Driver 13 for SQL Server};Server=tcp:oasis-data.database.windows.net,1433;Database=OasisTransaction;Uid=OasisData;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'OasisTransaction',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': 'oasis-data.database.windows.net',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'unicode_results': True,
#         },
#     },
# }
# Database={your_database}; Data Source=oasispgres.postgres.database.azure.com; User Id=oasisdata@oasispgres; Password={your_password}


# production start
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'HOST': os.environ.get('DB_HOST'),
#        'NAME': os.environ.get('DB_NAME'),
#        'USER': os.environ.get('DB_USER'),
#        'PASSWORD': os.environ.get('DB_PASS'),
#    }
#}
# production end

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': 'oasispgres.postgres.database.azure.com',
#         'NAME': 'postgres',
#         'USER': 'oasisdata@oasispgres',
#         'PASSWORD': 'Oa$i$Data',
#     }
# }

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CRONJOBS = [
    ('*/1 * * * *', 'octoparse.cron.my_scheduled_job', '>> ~/file.log')
] 
CRONTAB_COMMAND_SUFFIX = '2>&1'


AUTH_USER_MODEL = 'account.Account'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':12,

    'DEFAULT_FILTER_BACKENDS':  (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        ),
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',

}

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ORIGIN_WHITELIST = [
#     "http://52.154.246.210",
#     "52.154.246.210",
#     "https://oasiswebapp.azurewebsites.net"
# ]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = '/static/'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# local start
# Redis and Celery Conf
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
# local end


# production start
# Redis and Celery Conf
#CELERY_BROKER_URL = "redis://:Z1O+g54esQu1NciWQBDY+X8RQttcKHax3RyBtgJtX4M=@oasis.redis.cache.windows.net:6379"
#CELERY_RESULT_BACKEND = "redis://:Z1O+g54esQu1NciWQBDY+X8RQttcKHax3RyBtgJtX4M=@oasis.redis.cache.windows.net:6379"
# production end
