from laboite.settings import *  # noqa


# Use SQLite in-memory backend for tests
DATABASES['default'] = {  # noqa
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:'
}
