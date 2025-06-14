"""
Django settings for Meetbouten project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from azure.identity import WorkloadIdentityCredential

from .azure_settings import Azure

azure = Azure()

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
    "storages",
]
LOCAL_APPS = [
    "admin_chart",
    "bouwblokken",
    "metingen",
    "referentie_tabellen",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "media"))
MEDIA_URL = "/media/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
]

AUTHENTICATION_BACKENDS = [
    "main.auth.OIDCAuthenticationBackend",
]

## OpenId Connect settings ##
LOGIN_URL = "oidc_authentication_init"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL_FAILURE = "/static/403.html"

OIDC_BASE_URL = os.getenv("OIDC_BASE_URL")

OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET")
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = os.getenv("OIDC_RP_SCOPES")
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OIDC_BASE_URL}/oauth2/v2.0/authorize"
OIDC_OP_TOKEN_ENDPOINT = f"{OIDC_BASE_URL}/oauth2/v2.0/token"
OIDC_OP_USER_ENDPOINT = "https://graph.microsoft.com/oidc/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{OIDC_BASE_URL}/discovery/v2.0/keys"
OIDC_OP_LOGOUT_ENDPOINT = f"{OIDC_BASE_URL}/oauth2/v2.0/logout"
OIDC_OP_ISSUER = os.getenv("OIDC_OP_ISSUER")
OIDC_AUTH_REQUEST_EXTRA_PARAMS = {"prompt": "select_account"}
OIDC_USE_NONCE = False
OIDC_VERIFY_AUDIENCE = os.getenv("OIDC_VERIFY_AUDIENCE", True)
OIDC_TRUSTED_AUDIENCES = os.getenv("OIDC_TRUSTED_AUDIENCES", [])

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
DATABASE_OPTIONS = {"sslmode": "allow", "connect_timeout": 5}

# Check if we are using Azure Database for PostgreSQL, if so additional options are required
if DATABASE_HOST and DATABASE_HOST.endswith(".azure.com"):
    DATABASE_PASSWORD = azure.auth.db_password
    DATABASE_OPTIONS["sslmode"] = "require"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "CONN_MAX_AGE": 60 * 5,
        "PORT": DATABASE_PORT,
        "OPTIONS": DATABASE_OPTIONS,
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

# Django-storages for Django > 4.2
STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Azure Storageaccount settings
if os.getenv("AZURE_FEDERATED_TOKEN_FILE"):
    credential = WorkloadIdentityCredential()
    STORAGE_AZURE = {
        "default": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "token_credential": credential,
                "account_name": os.getenv("AZURE_STORAGE_ACCOUNT_NAME"),
                "azure_container": os.getenv("AZURE_CONTAINER"),
                "custom_domain": os.getenv("HOST_DOMAIN"),
            },
        },
    }
    STORAGES |= STORAGE_AZURE #update storages with storage_azure


DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

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
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
DJANGO_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "WARNING").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"],
    },
    "formatters": {
        "console": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "console",
        }
    },
    "loggers": {
        "metingen": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "bouwblokken": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "referentie_tabellen": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "admin_chart": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
        # Debug all batch jobs
        "doc": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "index": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "search": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "elasticsearch": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "urllib3": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "factory.containers": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "factory.generate": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "requests.packages.urllib3.connectionpool": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        # Log all unhandled exceptions
        "django.request": {
            "level": "DEBUG" if DEBUG else LOG_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
    "APPLICATIONINSIGHTS_CONNECTION_STRING"
)

if APPLICATIONINSIGHTS_CONNECTION_STRING:
    OPENCENSUS = {
        "TRACE": {
            "SAMPLER": "opencensus.trace.samplers.ProbabilitySampler(rate=1)",
            "EXPORTER": f"opencensus.ext.azure.trace_exporter.AzureExporter(connection_string='{APPLICATIONINSIGHTS_CONNECTION_STRING}')",
        }
    }
    LOGGING["handlers"]["azure"] = {
        "level": "DEBUG",
        "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
        "connection_string": APPLICATIONINSIGHTS_CONNECTION_STRING,
    }
    LOGGING["loggers"]["django"]["handlers"] = ["azure", "console"]
    LOGGING["loggers"]["metingen"]["handlers"] = ["azure", "console"]
    LOGGING["loggers"]["bouwblokken"]["handlers"] = ["azure", "console"]
    LOGGING["loggers"]["referentie_tabellen"]["handlers"] = ["azure", "console"]
    LOGGING["loggers"]["admin_chart"]["handlers"] = ["azure", "console"]
