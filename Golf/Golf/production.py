from .settings import *
import sys
import heroku_db

DATABASES["default"] = heroku_db.database(False, True)
