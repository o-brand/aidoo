import os
import heroku_db
from .settings import *


# Database
DATABASES["default"] = heroku_db.database(False, True)


# For security (run python manage.py check --deploy to check the problems)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# EMAIL BACKEND
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "aidoo.scot@gmail.com"
EMAIL_USE_TLS = True

# Password
if os.environ.get("EMAIL_PASSWORD") is not None:
    password = os.environ["EMAIL_PASSWORD"]
else:
    password = ""

EMAIL_HOST_PASSWORD = password
