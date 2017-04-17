DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
SECRET_KEY = "r4dy"
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'tests'
]
