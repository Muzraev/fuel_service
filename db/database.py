"""Подключение к отдельной предметной базе и выполнение SQL."""

import sqlite3
from contextlib import closing
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'data' / 'fuel_service.sqlite'
SQL_DIR = BASE_DIR / 'sql'


def get_connection(path=None):
    """Открыть соединение с именованными строками и проверкой связей."""
    connection = sqlite3.connect(path if path is not None else DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def init_database(path=None):
    """Создать отсутствующие таблицы, сохранив существующие записи."""
    with closing(get_connection(path)) as connection:
        connection.executescript(
            (SQL_DIR / 'schema.sql').read_text(encoding='utf-8')
        )


def load_queries():
    """Прочитать именованные запросы из единственного SQL-источника."""
    queries = {}
    for section in (SQL_DIR / 'queries.sql').read_text(
        encoding='utf-8'
    ).split('-- name: ')[1:]:
        name, statement = section.split('\n', 1)
        queries[name.strip()] = statement.strip()
    return queries


QUERIES = load_queries()


def fetch_all(name, parameters=()):
    """Выполнить известный запрос; значения передаются отдельно от SQL."""
    with closing(get_connection()) as connection:
        return connection.execute(QUERIES[name], parameters).fetchall()


def fetch_one(name, parameters=()):
    """Получить одну именованную строку или None."""
    rows = fetch_all(name, parameters)
    return rows[0] if rows else None


if __name__ == '__main__':
    init_database()
    print(f'База данных готова: {DB_PATH}')
