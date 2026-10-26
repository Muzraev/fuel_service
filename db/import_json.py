"""Запуск из корня проекта: python -m db.import_json."""

import json
from contextlib import closing

from db.database import BASE_DIR, DB_PATH, get_connection, init_database


def import_json(data_dir=None, database_path=None):
    """Импортировать новые ID атомарно, не заменяя имеющиеся записи."""
    data_dir = BASE_DIR / 'data' if data_dir is None else data_dir
    init_database(database_path)
    # Имена таблиц и полей заданы программой, пользовательских значений нет.
    tables = {
        'cars': ('id', 'name'),
        'fuels': ('id', 'name'),
        'consumptions': ('id', 'car_id', 'liters_per_100km'),
        'refuelings': (
            'id', 'car_id', 'fuel_id', 'fuel_liters', 'price_per_liter'
        ),
    }
    counts = {}
    with closing(get_connection(database_path)) as connection:
        with connection:
            for table, fields in tables.items():
                records = json.loads(
                    (data_dir / f'{table}.json').read_text(encoding='utf-8')
                )
                placeholders = ', '.join('?' for _ in fields)
                connection.executemany(
                    f'INSERT INTO {table} ({", ".join(fields)}) '
                    f'VALUES ({placeholders}) ON CONFLICT(id) DO NOTHING',
                    [tuple(record[field] for field in fields)
                     for record in records],
                )
                counts[table] = connection.execute(
                    f'SELECT COUNT(*) FROM {table}'
                ).fetchone()[0]
    return counts


if __name__ == '__main__':
    print(f'Импорт в {DB_PATH}: {import_json()}')
