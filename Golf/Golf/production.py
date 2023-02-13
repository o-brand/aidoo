from .settings import *
import sys
import heroku_db

# Database
DATABASES["default"] = heroku_db.database(False, True)


# For security (run python manage.py check --deploy to check the problems)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
