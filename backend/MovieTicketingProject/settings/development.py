# MovieTicketingProject/settings/development.py

from .base import *
from decouple import config, Csv # Csv is useful for parsing comma-separated values
from dj_database_url import parse as db_url # For parsing database URL strings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool) # Get DEBUG from .env

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv()) # Get ALLOWED_HOSTS from .env

# Install dj-database-url: pipenv install dj-database-url
# MySQL Database configuration for development
# Using DATABASE_URL environment variable for database connection
DATABASES = {
    'default': config('DATABASE_URL', cast=db_url) # Reads DATABASE_URL from .env
}

# Add CORS Headers settings for React frontend
# You'll need to install django-cors-headers: pipenv install django-cors-headers
INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv(), default='http://localhost:3000,http://127.0.0.1:3000')

# Or, if you need to allow all origins during early development (less secure)
# CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Allow credentials (cookies, HTTP authentication) to be sent with cross-origin requests
CORS_ALLOW_CREDENTIALS = True


# You might want to override STATIC_ROOT for development
# STATIC_ROOT = BASE_DIR / 'static_dev' # Already set in base to a good default

# Log all SQL queries to console during development (useful for debugging)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False, # Prevent duplicate logging
        },
    },
}