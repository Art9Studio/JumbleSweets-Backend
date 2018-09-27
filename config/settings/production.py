from .base import *  # noqa
# from .base import env

ENABLE_SSL = get_bool_from_env('ENABLE_SSL', False)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG

loaders = [
    'django.template.loaders.cached.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader']


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': context_processors,
        'loaders': loaders,
        'string_if_invalid': ''}}]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://saleor:saleor@localhost:5432/saleor',
        conn_max_age=600)}

REDIS_URL = os.environ.get('REDIS_URL')
if REDIS_URL:
    CACHE_URL = os.environ.setdefault('CACHE_URL', REDIS_URL)
CACHES = {'default': django_cache_url.config()}

# support deployment-dependant elastic enviroment variable
ES_URL = (os.environ.get('ELASTICSEARCH_URL') or
          os.environ.get('SEARCHBOX_URL') or os.environ.get('BONSAI_URL'))

ENABLE_SEARCH = bool(ES_URL) or DB_SEARCH_ENABLED  # global search disabling

if ES_URL:
    SEARCH_BACKEND = 'saleor.search.backends.elasticsearch'
    INSTALLED_APPS.append('django_elasticsearch_dsl')
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': ES_URL}}

