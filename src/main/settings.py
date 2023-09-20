"""
Django settings for Meetbouten project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from .azure_settings import Azure

azure = Azure()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", False))

ALLOWED_HOSTS = ["*"]
X_FRAME_OPTIONS = "ALLOW-FROM *"
INTERNAL_IPS = ("127.0.0.1", "0.0.0.0")
DATA_UPLOAD_MAX_MEMORY_SIZE = (
    1024 * 1024 * 20
)  # max upload size; 20MB (instead of the default 2.5MB)
IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = True

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
]
THIRD_PARTY_APPS = [
    "import_export",
    "leaflet",
    "mozilla_django_oidc",  # load after django.contrib.auth!
]
LOCAL_APPS = [
    "admin_chart",
    "bouwblokken",
    "metingen",
    "referentie_tabellen",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace("\\", "/")
MEDIA_URL = "/media/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'mozilla_django_oidc.middleware.SessionRefresh'
]

AUTHENTICATION_BACKENDS = [
    'main.auth.OIDCAuthenticationBackend',
]

## OpenId Connect settings ##
LOGIN_URL = 'oidc_authentication_init'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL_FAILURE = '/static/403.html'

OIDC_BASE_URL = os.getenv('OIDC_BASE_URL')
OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET')
OIDC_OP_AUTHORIZATION_ENDPOINT = f'{OIDC_BASE_URL}/oauth2/v2.0/authorize'
OIDC_OP_TOKEN_ENDPOINT = f'{OIDC_BASE_URL}/oauth2/v2.0/token'
OIDC_OP_USER_ENDPOINT = 'https://graph.microsoft.com/oidc/userinfo'
OIDC_OP_JWKS_ENDPOINT = f'{OIDC_BASE_URL}/discovery/v2.0/keys'
OIDC_OP_LOGOUT_ENDPOINT = f'{OIDC_BASE_URL}/oauth2/v2.0/logout'
OIDC_RP_SIGN_ALGO = 'RS256'


ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src/metingen/../admin_chart/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "main.urls"
BASE_URL = os.getenv("BASE_URL", "")
FORCE_SCRIPT_NAME = BASE_URL

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_HOST = os.getenv("DATABASE_HOST", "database")
DATABASE_NAME = os.getenv("DATABASE_NAME", "meetbouten")
DATABASE_USER = os.getenv("DATABASE_USER", "meetbouten")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "insecure")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_OPTIONS = {'sslmode': 'allow', 'connect_timeout': 5}

if 'azure.com' in DATABASE_HOST:
    DATABASE_PASSWORD = azure.auth.db_password
    DATABASE_OPTIONS['sslmode'] = 'require'

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "CONN_MAX_AGE": 60 * 5,
        "PORT": DATABASE_PORT,
        'OPTIONS': DATABASE_OPTIONS,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = BASE_URL + "/static/"
STATIC_ROOT = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    }
}

if DEBUG:
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE += (
        # 'corsheaders.middleware.CorsMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )
    CORS_ORIGIN_ALLOW_ALL = True
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]


# AZURE
AZURE_CONNECTION_STRING = os.getenv(
    "AZURE_BLOB_CONNECTION_STRING"
)  # Note: Key and variable name differ
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")
if AZURE_CONNECTION_STRING:
    DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
    STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"

IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = True

# Leaflet settings
LEAFLET_CONFIG = {
    "TILES": [
        (
            "Amsterdam",
            "https://t1.data.amsterdam.nl/topo_wm_light/{z}/{x}/{y}.png",
            {
                "attribution": 'Kaartgegevens &copy; <a href="https://data.amsterdam.nl/">Gemeente Amsterdam </a>'
            },
        ),
    ],
    "DEFAULT_CENTER": (4.9020727, 52.3717204),
    "DEFAULT_ZOOM": 12,
    "MIN_ZOOM": 11,
    "MAX_ZOOM": 21,
    "SPATIAL_EXTENT": (3.2, 50.75, 7.22, 53.7),
    "RESET_VIEW": False,
}

# Django Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'sentry'],
    },
    'formatters': {
        'console': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'metingen': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': True,
        },
        'bouwblokken': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': True,
        },
        'referentie_tabellen': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': True,
        },
        'admin_chart': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': os.getenv(
                'DJANGO_LOG_LEVEL', 'ERROR' if 'pytest' in sys.argv[0] else 'INFO'
            ).upper(),
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        # Debug all batch jobs
        'doc': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'index': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'search': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'elasticsearch': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'urllib3': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'factory.containers': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'factory.generate': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'requests.packages.urllib3.connectionpool': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        # Log all unhandled exceptions
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
    'APPLICATIONINSIGHTS_CONNECTION_STRING'
)

if APPLICATIONINSIGHTS_CONNECTION_STRING:
    OPENCENSUS = {
        'TRACE': {
            'SAMPLER': 'opencensus.trace.samplers.ProbabilitySampler(rate=1)',
            'EXPORTER': f"opencensus.ext.azure.trace_exporter.AzureExporter(connection_string='{APPLICATIONINSIGHTS_CONNECTION_STRING}')",
        }
    }
    LOGGING['handlers']['azure'] = {
        'level': "DEBUG",
        'class': "opencensus.ext.azure.log_exporter.AzureLogHandler",
        'connection_string': APPLICATIONINSIGHTS_CONNECTION_STRING,
    }
    LOGGING['loggers']['django']['handlers'] = ['azure', 'console']
    LOGGING['loggers']['metingen']['handlers'] = ['azure', 'console']
    LOGGING['loggers']['bouwblokken']['handlers'] = ['azure', 'console']
    LOGGING['loggers']['referentie_tabellen']['handlers'] = ['azure', 'console']
    LOGGING['loggers']['admin_chart']['handlers'] = ['azure', 'console']

# Sentry logging
sentry_dsn = os.getenv('SENTRY_DSN')
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=os.getenv('ENVIRONMENT', 'dev'),
        release=os.getenv('VERSION', 'dev'),
        integrations=[
            DjangoIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
