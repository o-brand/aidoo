"""Django settings for Aidoo project."""

from pathlib import Path
import os
import sys


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ygkairtzpyop9eyg6n&1xd6@i*2mn1jfuq&b(jy!4*g9q6sa=f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    "teamgolf.pythonanywhere.com",
    "127.0.0.1",
    "aidoo.herokuapp.com",
]


# OUR EXTENDED USER
AUTH_USER_MODEL = "userprofile.User"


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "login.apps.LoginConfig",
    "jobs.apps.JobsConfig",
    "userprofile.apps.UserprofileConfig",
    "chat.apps.ChatConfig",
    "store.apps.StoreConfig",
    "superadmin.apps.SuperadminConfig",
    "help.apps.HelpConfig",
    "vendor.apps.VendorConfig",
    "profanity",
    "cloudinary_storage",
    "cloudinary",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "Aidoo.middlewares.LoginRequiredMiddleware",
]

ROOT_URLCONF = "Aidoo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "Aidoo.processors.auth", # To have "me" in the templates.
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "Aidoo.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

import heroku_db

DATABASES = {"default": heroku_db.database("test" in sys.argv, False)}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Media files (uploaded by users)
# https://pypi.org/project/django-cloudinary-storage/

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "htylsn6uq",
    "API_KEY": "788656644488616",
    "API_SECRET": "qbkrT2mfRDOBbHAXNj0MfDTaeVc",
}

# Tests will not reach cloudinary
if "test" in sys.argv:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "home"  # After login, the user is redirected to here.
LOGOUT_REDIRECT_URL = "/"  # After log out, the user is redirected to here.


# EMAIL BACKEND for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# VENDOR KEYS
KEY = b'K7gzDFlFHb3Y7uANnSQORZIQnX8c6WqWMH9jtD4oqr8='

# SITE ID
SITE_ID = 2


# CHAT
# The maximum number of days of storing a message
CHAT_MESSAGE_TTL = 91


# HEROKU
if os.environ.get("HOME") is not None and "/app" in os.environ["HOME"]:
    import django_heroku

    django_heroku.settings(locals())

    DEBUG = False
    DEBUG_PROPAGATE_EXCEPTIONS = True # We can see the errors in the logs.
    KEY = str.encode(os.environ.get("KEY"))
    SECRET_KEY = os.environ.get("SECRET")
    SITE_ID = 1
