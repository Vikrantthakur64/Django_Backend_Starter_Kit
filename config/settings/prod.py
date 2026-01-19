from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES['default'] = dj_database_url.config(default='sqlite:///db.sqlite3')
DATABASES['default']['CONN_MAX_AGE'] = 600 