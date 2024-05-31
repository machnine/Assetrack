""" production settings """
import os

# pylint: disable=wildcard-import, unused-wildcard-import
from .base import *  # noqa: F403

# Debug mode
DEBUG = False

# Secret key for production
SECRET_KEY = os.environ.get("SECRET_KEY")

# Allowed hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CSRF settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"
# Set the CSRF_TRUSTED_ORIGINS to the domain of the website
CSRF_TRUSTED_ORIGINS = []

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 15  # 15 minutes
SESSION_COOKIE_SECURE = True

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {"class": "logging.FileHandler", "filename": os.getenv("DJANGO_LOG", "debug.log")},
    },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": "WARNING"},
    },
}
