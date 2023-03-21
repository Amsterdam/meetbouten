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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
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
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 20  # max upload size; 20MB (instead of the default 2.5MB)
IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export",
    "referentie_tabellen",
    "metingen",
    "bouwblokken",
    "admin_chart",
    "django.contrib.gis",
    "leaflet"
]

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
]

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

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("DATABASE_NAME", "meetbouten"),
        "USER": os.getenv("DATABASE_USER", "meetbouten"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "insecure"),
        "HOST": os.getenv("DATABASE_HOST", "database"),
        "CONN_MAX_AGE": 20,
        "PORT": os.getenv("DATABASE_PORT", "5432"),
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


REST_FRAMEWORK = dict(
    PAGE_SIZE=20,
    MAX_PAGINATE_BY=100,
    UNAUTHENTICATED_USER={},
    UNAUTHENTICATED_TOKEN={},
    DEFAULT_AUTHENTICATION_CLASSES=("contrib.rest_framework.authentication.SimpleTokenAuthentication",),
    DEFAULT_PAGINATION_CLASS="datapunt_api.pagination.HALPagination",
    DEFAULT_RENDERER_CLASSES=(
        "rest_framework.renderers.JSONRenderer",
        "datapunt_api.renderers.PaginatedCSVRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_xml.renderers.XMLRenderer",  # must be lowest!
    ),
    DEFAULT_FILTER_BACKENDS=(
        # 'rest_framework.filters.SearchFilter',
        # 'rest_framework.filters.OrderingFilter',
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    DEFAULT_VERSIONING_CLASS="rest_framework.versioning.NamespaceVersioning",
    COERCE_DECIMAL_TO_STRING=True,
)

#AZURE
AZURE_CONNECTION_STRING = os.getenv("AZURE_BLOB_CONNECTION_STRING")  # Note: Key and variable name differ
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")
if AZURE_CONNECTION_STRING:
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = True
