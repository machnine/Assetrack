"""Custom command to load fixtures"""

from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load fixtures"

    def handle(self, *args, **options):
        fixtures = Path("fixtures")
        for fixture in fixtures.iterdir():
            call_command("loaddata", fixture)
            self.stdout.write(self.style.SUCCESS(f"Fixture {fixture} loaded"))
