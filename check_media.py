"""
Quick diagnostic to check media configuration
"""
import os
import sys
from pathlib import Path

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / '.env')
except:
    pass

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')

import django
django.setup()

from django.conf import settings
from django.urls import get_resolver

print("=== Media Configuration ===")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")

print("\n=== Check File Exists ===")
test_file = Path(settings.MEDIA_ROOT) / "attachments/documents/C6_Temperature_monitoring_floor_plan_ver14_Dec23.jpg"
print(f"Looking for: {test_file}")
print(f"Exists: {test_file.exists()}")

print("\n=== URL Patterns with 'media' ===")
resolver = get_resolver()
for pattern in resolver.url_patterns:
    pattern_str = str(pattern.pattern)
    if 'media' in pattern_str.lower():
        print(f"  {pattern_str}")

print("\n=== Test URL Resolution ===")
from django.urls import resolve
try:
    match = resolve('/media/attachments/documents/test.jpg')
    print(f"URL resolves to: {match}")
except Exception as e:
    print(f"URL resolution failed: {e}")
