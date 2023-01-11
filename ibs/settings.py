"""
Django settings for ibs project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta, tzinfo
from celery.schedules import crontab
from rest_framework.settings import api_settings
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&qgo(#j^su+@nr@gtdu9c=su(l7ci_3xttd5u@rwx@b6k($_#h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # dependencies
    'django_celery_beat',
    'django_celery_results',
    'polymorphic',    
    'corsheaders',
    'rest_framework',
    'knox',

    # Important apps for the working of ibs
    'ibs.users',
    'ibs.tools',
    # apps
    'ibs.financial',
    'ibs.activity',
    'ibs.chugs',
    'ibs.maluspunten'
]

# user model
AUTH_USER_MODEL = 'users.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'ibs.tools.middleware.DisableCSRFMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8000',
]

CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_AGE = 1209600 # 2 weken


ROOT_URLCONF = 'ibs.urls'

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

WSGI_APPLITION = 'ibs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'NAME': os.getenv('DB_NAME', 'ibs'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}


# 
# IBS settings!
# 
COMMITTEE_ABBREVIATION_SENATE = 'senaat'
COMMITTEE_ABBREVIATION_ADMINS = 'admins'
COMMITTEE_ABBREVIATION_COLOSSEUM = 'colosseum'
COMMITTEE_ABBREVIATION_FINANCIE = 'financie'
COMMITTEE_ABBREVIATION_ICT = 'ict'
COMMITTEE_ABBREVIATION_MEMBER = 'members'
COMMITTEE_ABBREVIATION_ASPIRING_MEMBER = 'aspiring'

DEFAULT_IBS_USER_USERNAME = 'ibs'
DEFAULT_IBS_USER_EMAIL = 'ibs@oddinvictus.nl'

MONTHLY_CONTRIBUTION = 6.00

# Celery settings

CELERY_TIMEZONE= "Europe/Amsterdam"
CELERY_TASK_TRACK_STARTED = True
CELETER_TASK_TIME_LIMIT = 30 * 60

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672')

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    # Collect monthly contribution every 1st of the month at 12:00
    'collect_monthly_contribution': {
        'task': 'ibs.financial.tasks.collect_monthly_contribution',
        'schedule': crontab(minute=0, hour=12, day_of_month='1'),
        'options': {
            'expires': 60
        },
    },
    'test': {
        'task': 'ibs.financial.tasks.test',
        'schedule': crontab(minute='*/1'),
        'options': {
            'expires': 60
        },
    },
    # Double the strafbakken every 1st of the month at 01:00
    'double_strafbakken': {
        'task': 'ibs.chugs.tasks.double_strafbakken',
        'schedule': crontab(minute=0, hour=1, day_of_month='1'),
        'options': {
            'expires': 60
        },
    }
}

try:
    from ibs.local_settings import *
except ImportError:
    pass