"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    dotenv_path = Path(__file__).resolve().parent.parent / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
except ImportError:
    pass  # python-dotenv not installed

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
