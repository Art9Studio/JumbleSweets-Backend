from .base import *  # noqa

# from .base import env
load_dotenv(str(ROOT_DIR.path('.envs/.local/.django')))
load_dotenv(str(ROOT_DIR.path('.envs/.local/.postgres')))

DEBUG = True

ENABLE_SSL = False

SECURE_SSL_REDIRECT = False

loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader']

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': context_processors,
        'loaders': loaders,
        'string_if_invalid': '<< MISSING VARIABLE "%s" >>'}}]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ODzdplLkQFL4PeCefH5CiOVe6x1jKeq9u3F4nWWmHuywkLxfQHHFUZa61i7Ew5DB')

MIDDLEWARE.append(
    'debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.append('debug_toolbar')
# MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
# INSTALLED_APPS.append('corsheaders')
# CORS_ORIGIN_WHITELIST = ( 'localhost:8080', )
DEBUG_TOOLBAR_PANELS = [
    # adds a request history to the debug toolbar
    'ddt_request_history.panels.request_history.RequestHistoryPanel',

    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'RESULTS_STORE_SIZE': 100}

ENABLE_SILK = get_bool_from_env('ENABLE_SILK', False)
if ENABLE_SILK:
    MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware')
    INSTALLED_APPS.append('silk')

DATABASES = {
    'default': dj_database_url.config(
        default=f'postgres://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@{os.environ.get("POSTGRES_DEBUG_HOST")}:{os.environ.get("POSTGRES_PORT")}/{os.environ.get("POSTGRES_DB")}',
        conn_max_age=600)}
DATABASES['default']['ATOMIC_REQUESTS'] = True

