"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import socket
import os
import logging

from django.conf.locale.en import formats as en_formats

from . import database


# If the host name starts with 'live', DJANGO_HOST = "production"
if socket.gethostname().startswith('ubuntu-s-1vcpu-1gb-blr1'):
    DJANGO_HOST = "production"
# Else if host name starts with 'test', set DJANGO_HOST = "test"
elif socket.gethostname().startswith('test'):
    DJANGO_HOST = "testing"
else:
    # If host doesn't match, assume it's a development server, set DJANGO_HOST = "development"
    DJANGO_HOST = "development"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('RHCAPP_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if DJANGO_HOST == "production":
    DEBUG = False
else:
    DEBUG = True


ALLOWED_HOSTS = ['localhost', 'app.rasayu.com']  # '174.138.123.39'


if DJANGO_HOST == "production":
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'appapi',
    'webapp',  # keep before `adminlte3`, `allauth`

    # https://github.com/d-demirci/django-adminlte3
    # General use templates & template tags (should appear first)
    'adminlte3',
    # Optional: Django admin theme (must be before django.contrib.admin)
    'adminlte3_theme',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # needed by `allauth`

    'allauth',  # https://django-allauth.readthedocs.io/en/latest/installation.html
    'allauth.account',
    'allauth.socialaccount',
    # ... include the social auth providers you want to enable

    'rest_framework',  # https://www.django-rest-framework.org/

    'crispy_forms',  # https://django-crispy-forms.readthedocs.io/en/latest/install.html
]


# https://django-crispy-forms.readthedocs.io/en/latest/install.html
CRISPY_TEMPLATE_PACK = 'bootstrap4'


SITE_ID = 1  # `allauth`
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'


# https://django-adminlte2.readthedocs.io/en/latest/templates_and_blocks.html
LOGOUT_URL = '/accounts/logout/'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # needed by `allauth`
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': database.config()
}


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

LANGUAGE_CODE = 'en-in'  # 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

en_formats.DATE_INPUT_FORMATS = (
    "%d/%m/%Y", "%d/%n/%Y",
    "%j/%m/%Y", "%j/%n/%Y",
    "%d/%m/%y", "%d/%n/%y",
    "%j/%m/%y", "%j/%n/%y"
)
en_formats.DATE_FORMAT = 'd/m/Y'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.getenv('RHCAPP_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.getenv('RHCAPP_EMAIL_HOST_USER')
EMAIL_SUBJECT_PREFIX = '[Ras??yu] '

ADMINS = [('Admin', os.getenv('RHCAPP_ADMIN_1_EMAIL')), ]


DJANGO_LOGGER = logging.getLogger('django')


CRF_API_URL_BASE = os.getenv(
    'CRF_API_URL_HOST',
    'http://localhost:8000/rhcapi/')
CRF_API_HEADERS = {
    'Authorization': 'Token ' + os.getenv('RHCAPP_AUTH_TOKEN', ''),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
