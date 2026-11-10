"""Проверки SQL-слоя и страниц без обращения к рабочей базе проекта."""

import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuel_service_web.settings')

import django  # noqa: E402
from django.test import Client, override_settings  # noqa: E402

from db import database  # noqa: E402
from db.import_json import import_json  # noqa: E402

django.setup()


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        settings = override_settings(ALLOWED_HOSTS=['testserver'])
        settings.enable()
        self.addCleanup(settings.disable)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.patch = patch.object(database, 'DB_PATH', self.path)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        import_json()
        with closing(database.get_connection()) as connection:
            with connection:
                connection.execute(
                    "INSERT INTO cars VALUES (2, 'No refuelings')"
                )
                connection.execute(
                    'INSERT INTO refuelings VALUES (2, 1, 1, 10, 60)'
                )
        self.client = Client()

    def test_repeat_import_preserves_existing_data(self):
        self.assertEqual(import_json(), {
            'cars': 2, 'fuels': 1, 'consumptions': 1, 'refuelings': 2,
        })
        database.init_database()
        self.assertEqual(database.fetch_one('totals')['total_cost'], 3200)

    def test_constraints_and_named_rows(self):
        with closing(database.get_connection()) as connection:
            self.assertEqual(
                connection.execute('PRAGMA foreign_keys').fetchone()[0], 1
            )
            for sql in (
                'INSERT INTO refuelings VALUES (3, 999, 1, 10, 50)',
                'INSERT INTO refuelings VALUES (3, 1, 1, 0, 50)',
                'INSERT INTO consumptions VALUES (2, 1, 8)',
            ):
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(sql)
        self.assertIsInstance(database.fetch_one('totals'), sqlite3.Row)

    def test_all_queries_and_aggregates(self):
        parameters = {
            'car_detail': (1,), 'refueling_detail': (1,),
            'search': (1, 1, 1, 1, 20), 'frequent_cars': (1,),
        }
        for name in database.QUERIES:
            with self.subTest(query=name):
                self.assertIsInstance(
                    database.fetch_all(name, parameters.get(name, ())), list
                )
        self.assertEqual(database.fetch_one('totals')['count'], 2)
        self.assertEqual(database.fetch_one('totals')['average_cost'], 1600)
        self.assertEqual(database.fetch_all('by_car')[1]['count'], 0)
        self.assertEqual(database.fetch_all('by_fuel')[0]['total_liters'], 50)
        self.assertEqual(database.fetch_all('without_refuelings')[0]['id'], 2)
        self.assertEqual(len(database.fetch_all('frequent_cars', (1,))), 1)
        self.assertEqual(database.fetch_all('frequent_cars', (2,)), [])

    def test_import_rolls_back_on_invalid_relationship(self):
        source = Path(self.temp.name)
        for name in ('cars', 'fuels', 'consumptions', 'refuelings'):
            data = json.loads(
                (database.BASE_DIR / 'data' / f'{name}.json').read_text(
                    encoding='utf-8'
                )
            )
            if name == 'cars':
                data.append({'id': 3, 'name': 'Must roll back'})
            if name == 'refuelings':
                data.append({
                    'id': 3, 'car_id': 999, 'fuel_id': 1,
                    'fuel_liters': 10, 'price_per_liter': 50,
                })
            (source / f'{name}.json').write_text(
                json.dumps(data), encoding='utf-8'
            )
        with self.assertRaises(sqlite3.IntegrityError):
            import_json(source)
        self.assertIsNone(database.fetch_one('car_detail', (3,)))
