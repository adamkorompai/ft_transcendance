"""
Django settings for ft_transcendence project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from os import environ
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+f_x^6-&#=vue%lsu4^uzx$$#932dey&^=-%jcg#xvm7)diwii'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = '/'  # Replace 'home' with the name of the URL you want to redirect to.

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    "crispy_bootstrap5",
    'home',
    'channels',
    'channels_postgres',
    'chatapp',
    'accounts',
    'pong',
    'stats',
    'django_prometheus',
    'django_extensions',
    'sslserver',
]

ASGI_APPLICATION = 'ft_transcendence.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_postgres.core.PostgresChannelLayer',
        'CONFIG': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': environ.get('POSTGRES_DB'),
            'USER': environ.get('POSTGRES_USER'),
            'PASSWORD': environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': '',

            }
        },
    }

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'ft_transcendence.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'ft_transcendence.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('POSTGRES_DB'),
        'USER': environ.get('POSTGRES_USER'),
        'PASSWORD': environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '',
    },
    	'channels_postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('POSTGRES_DB'),
        'USER': environ.get('POSTGRES_USER'),
        'PASSWORD': environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '',
	}
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prometheus scraping

PROMETHEUS_LATENCY_BUCKETS = (0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 25.0, 50.0, 75.0, float("inf"),)
PROMETHEUS_METRIC_NAMESPACE = "transcendance"