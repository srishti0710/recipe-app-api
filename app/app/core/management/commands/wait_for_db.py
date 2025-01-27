from psycopg2 import OperationalError as Psycopg2OpError
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand): 
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            db_up = False
        while db_up is False:
            try:
                db_conn = connections['default']
            except (OperationalError, Psycopg2OpError):
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))