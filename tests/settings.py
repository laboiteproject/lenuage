from laboite.settings import *


# Use SQLite in-memory backend for tests
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:'
}
