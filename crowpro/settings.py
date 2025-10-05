import sys
from pathlib import Path
from . import ckeditor_config as ck
from datetime import timedelta
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
DROPBOX_OAUTH2_REFRESH_TOKEN = os.getenv("DROPBOX_OAUTH2_REFRESH_TOKEN")
DROPBOX_OAUTH2_TOKEN = os.getenv("DROPBOX_OAUTH2_TOKEN")

DEBUG = os.getenv("DEBUG", False) == "True"
STATIC_ROOT = BASE_DIR

if DEBUG:
    from .dev import *

    logger.info("Running in development mode")
else:
    from .production import *

    logger.info("Running in production mode")

CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "upload_file"
CKEDITOR_5_CONFIGS = ck.CKEDITOR_5_CONFIGS
CKEDITOR_5_FILE_UPLOAD_PERMISSION = ck.CKEDITOR_5_FILE_UPLOAD_PERMISSION
CKEDITOR_5_FILE_STORAGES = ck.STORAGES

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'admincharts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'api',
    'authentication',
    'blog',
    'logs',
    'django_ckeditor_5',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'storages',
    'drf_yasg',
    'django_user_agents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'logs.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'crowpro.urls'

TEMPLATE_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'crowpro.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.auth.CookieJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SIMPLE_JWT = {
    "TOKEN_BLACKLIST_ENABLED": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=1800),
    "REFRESH_TOKEN_LIFETIME": timedelta(seconds=30*24*60*60),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": True
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'users.User'

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

DJANGO_LOG_LEVEL = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Keep Django's default loggers
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'local.log') if DEBUG else BASE_DIR / 'server.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {  # HTTP errors
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {  # SQL queries
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',  # change to INFO in prod
            'propagate': False,
        },
        'api': {  # your app-specific logs
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'authentication': {  # your app-specific logs
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'blog': {  # your app-specific logs
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'users': {  # your app-specific logs
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
