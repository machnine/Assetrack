"""
Windows WSGI server entry point using waitress.
This script is used for running Assetrack on Windows servers.
"""
import os
import sys
from waitress import serve

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the WSGI application
from core.wsgi import application

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('WSGI_HOST', '0.0.0.0')
    port = int(os.environ.get('WSGI_PORT', '8000'))
    threads = int(os.environ.get('WSGI_THREADS', '4'))

    print(f"Starting Assetrack on {host}:{port} with {threads} threads")
    print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE', 'core.settings.production')}")

    serve(
        application,
        host=host,
        port=port,
        threads=threads,
        url_scheme='http',
        _quiet=False
    )
