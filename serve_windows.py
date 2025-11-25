"""
Windows WSGI server entry point using waitress.
Simple port-based deployment with WhiteNoise serving static files.
"""
import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    dotenv_path = Path(__file__).resolve().parent / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print(f"[OK] Loaded .env from: {dotenv_path}")
    else:
        print(f"[WARN] .env file not found at: {dotenv_path}")
except ImportError:
    print("[WARN] python-dotenv not installed, using system environment variables")

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from waitress import serve
from core.wsgi import application

if __name__ == '__main__':
    host = os.environ.get('WSGI_HOST', '0.0.0.0')
    port = int(os.environ.get('WSGI_PORT', '7111'))
    threads = int(os.environ.get('WSGI_THREADS', '4'))

    print(f"[INFO] Starting Assetrack on {host}:{port} with {threads} threads")
    print(f"[INFO] Django settings: {os.environ.get('DJANGO_SETTINGS_MODULE', 'core.settings.production')}")
    print(f"[INFO] Static files served by WhiteNoise")

    serve(
        application,
        host=host,
        port=port,
        threads=threads,
        url_scheme='http',
        _quiet=False
    )
