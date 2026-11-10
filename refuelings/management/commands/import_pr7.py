"""Read-only source, atomic ORM import preserving IDs and relationships."""
import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cars.models import Car, Consumption
from fuels.models import Fuel
from refuelings.models import Refueling


class Command(BaseCommand):
    help = 'Перенос SQLite ПР7 в новую ORM-базу без изменения источника'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=Path,
                            default=settings.BASE_DIR / 'data'
                            / 'fuel_service.sqlite')

    def handle(self, *args, **options):
        source = options['source'].resolve()
        if not source.is_file():
            raise CommandError('Исходная база не найдена')
        tables = [('cars', Car), ('fuels', Fuel),
                  ('consumptions', Consumption), ('refuelings', Refueling)]
        with closing(sqlite3.connect(source.as_uri() + '?mode=ro',
                                     uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            try:
                with transaction.atomic():
                    for table, model in tables:
                        # Table names are fixed constants, never user input.
                        for row in conn.execute('SELECT * FROM ' + table):
                            data = dict(row)
                            pk = data.pop('id')
                            obj, created = model.objects.get_or_create(
                                pk=pk, defaults=data)
                            if not created and any(
                                getattr(obj, k) != v for k, v in data.items()
                            ):
                                raise CommandError(
                                    f'Конфликт {table} id={pk}; '
                                    'перенос отменён')
                            obj.full_clean()
            except sqlite3.Error as exc:
                raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS('Перенос завершён'))
