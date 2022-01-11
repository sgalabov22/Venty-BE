"""
Django settings for venty project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from os.path import join
from pathlib import Path
import cloudinary
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w@#ny+_sy7u5#x4*z#ohj$qgf^vlxv46a^ku1sj&qug22artt)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    'users',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'venty.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

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

WSGI_APPLICATION = 'venty.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'venty_db',
#         'USER': 'postgres',
#         'PASSWORD': 'admin',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dfmagsmbmr5sai',
        'USER': 'rlbishlsvhlfjb',
        'PASSWORD': 'ed9e6123807a3bf084fdd0efc347a0eb1883dd2a7cf394988ee196a5f0a7f538',
        'HOST': 'ec2-34-255-21-191.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
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

CORS_ALLOWED_ORIGINS = [

    "http://localhost:8000",

    "http://localhost:4200",

    "https://venty.azurewebsites.net"

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

STATIC_URL = '/static/'

STATICFILES_DIRS = (join(BASE_DIR, 'static'),)

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

AUTH_USER_MODEL = 'users.Account'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CLIENT_ID = 'q4IWWRNxIBN48KIPrLPVSTkgbfxqgdlP9mKRCd0P'
# CLIENT_SECRET = '5sU91720XAwclBJlrDyyR5WqueUcbXxzpyvfB4AcJYPOy6jYEo9Kv2guRzNxV0naNxF8LZsXJhfB6bzxNq0rPbYfYjSkjkcrFTOzegaSU15Z6Rm052oRS58OzsSb6Hx8'
#

CLIENT_ID = 'm7B0ieEIgPEhji89FApNpjjrv3vKOJYrO5aLtKjV'
CLIENT_SECRET = 'Zw2A0YrCTMeix82mlBcBZnHxPtGo4wUQQ0AppabmE5OtNYKaI7IvnHFRkF9qXxrAl6Qmadhyn8wKpRIRaxNxDucAfybveHyHr0LnbgRRkYIjqAycLeRxCWIGF2rPIGAy'


cloudinary.config(
    cloud_name="dhavld11j",
    api_key="137955467533472",
    api_secret="zmrAQXommqofywnVJENgkIk9sx8",
    secure=True
)