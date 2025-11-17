from pathlib import Path
import os
from datetime import timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
import environ
import sys
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent  # Points to Interior_Server/
sys.path.insert(0, str(BASE_DIR))

env = environ.Env()
# On local dev, read from .env file. On Render/prod, the OS env vars are used directly.
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# Configure Cloudinary if credentials are present; skip gracefully if not.
try:
    cloudinary.config(
        cloud_name=env("CLOUDINARY_CLOUD_NAME"),
        api_key=env("CLOUDINARY_API_KEY"),
        api_secret=env("CLOUDINARY_API_SECRET"),
        secure=True
    )
except Exception as e:
    # Log warning but continue; Cloudinary is optional at settings import time.
    print(f"Warning: Cloudinary config skipped ({type(e).__name__}). Set CLOUDINARY_* env vars if needed.")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_ytl2gx8q@eg!#$&2#%3$^nd&ddc6!%v1eqgkk3ipy8&wg@g7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.core',
    'apps.company',
    'apps.projects',
    'apps.blog',
    'apps.cms',
    'apps.contact',
    'apps.estimation',
    'apps.ecommerce',
    'apps.api',
    'rest_framework',
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interior_backend.urls'

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

WSGI_APPLICATION = 'interior_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(
        os.environ["DATABASE_URL"],   # force use of Render’s variable
        conn_max_age=600,
        ssl_require=True,
    )
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

# JWT lifetimes via env, fallback to sensible defaults
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "15"))
REFRESH_TOKEN_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))
ROTATE_REFRESH_TOKENS = os.getenv("ROTATE_REFRESH_TOKENS", "True").lower() in ("1","true","yes")
# BLACKLIST_AFTER_ROTATION = os.getenv("BLACKLIST_AFTER_ROTATION", "True").lower() in ("1","true","yes")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # you can set default permission classes later
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_DAYS),
    "ROTATE_REFRESH_TOKENS": ROTATE_REFRESH_TOKENS,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID", default="")
SENDGRID_API_KEY = env.str("SENDGRID_API_KEY", default="")
DEFAULT_FROM_EMAIL = "karkinirvik@gmail.com"