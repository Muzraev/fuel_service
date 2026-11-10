# Сервис учета топлива

Индивидуальный проект по дисциплине «Технологии разработки приложений на базе фреймворков».
Автор: Музраев Санджи Мингиянович, ЭФБО-16-24, 2026.

Проект предназначен для учёта автомобилей, видов топлива, норм расхода и заправок.
Главная сущность — `Refueling`: заправка связывает автомобиль и топливо, содержит
объём и цену за литр. Стоимость вычисляется как произведение объёма и цены.

## Текущее состояние: ПР7

Веб-приложение получает данные через SQL и стандартную библиотеку `sqlite3`.
Django ORM для предметной области не используется. Сохранены приложения,
маршруты, шаблоны и статика ПР6. Добавлены поиск заправок и статистика.
Исходные классы `models/`, `storage.py`, JSON и консольная версия `main.py`
сохранены как предыдущая реализация. Консольная версия продолжает работать с JSON;
изменения в ней не синхронизируются с SQLite автоматически.

## Запуск

Из корня проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m db.database
python -m db.import_json
python manage.py migrate
python manage.py check
python manage.py runserver --insecure
```
Подключение к бд и проверка на связи внешних ключей (задание 2)
from db.database import get_connection
conn = get_connection()
conn.execute("PRAGMA foreign_keys").fetchone()[0]

conn.execute(
    "INSERT INTO refuelings (car_id, fuel_id, fuel_liters, price_per_liter) VALUES (?, ?, ?, ?)",
    (999999, 1, 10, 65)
)

conn.rollback()
conn.close()
exit()

проверка бд (задание 3)
python -m db.database
наличие таблиц 
python
from db.database import get_connection
conn = get_connection()
print([row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")])
conn.close()
exit()


проверка бд(задание 4)

from db.database import get_connection

# Подключаемся к базе данных
conn = get_connection()

# Показываем, какая база используется
print("База данных:")
print(conn.execute("PRAGMA database_list").fetchone()["file"])

# Получаем список автомобилей
print("\nАвтомобили:")
rows = conn.execute("SELECT id, name FROM cars").fetchall()

for row in rows:
    print(row["id"], row["name"])

conn.close()



Открыть http://127.0.0.1:8000/. В текущих настройках `DEBUG = False`, поэтому
`--insecure` нужен серверу разработки для раздачи статики. Для публикации этот
режим не предназначен. `migrate` создаёт только служебные таблицы Django в
`db.sqlite3`; предметные таблицы создаёт `sql/schema.sql` в отдельном файле
`data/fuel_service.sqlite`.

## Структура базы данных

| Таблица | Поля и типы | Назначение |
| --- | --- | --- |
| cars | id INTEGER PRIMARY KEY, name TEXT NOT NULL | Автомобили |
| fuels | id INTEGER PRIMARY KEY, name TEXT NOT NULL | Виды топлива |
| consumptions | id INTEGER PRIMARY KEY, car_id INTEGER NOT NULL UNIQUE, liters_per_100km REAL NOT NULL | Норма расхода автомобиля |
| refuelings | id INTEGER PRIMARY KEY, car_id INTEGER NOT NULL, fuel_id INTEGER NOT NULL, fuel_liters REAL NOT NULL, price_per_liter REAL NOT NULL | Заправки |

Внешние ключи: `consumptions.car_id → cars.id`, `refuelings.car_id → cars.id`,
`refuelings.fuel_id → fuels.id`. Один автомобиль имеет не более одной нормы расхода
и любое число заправок. У вида топлива может быть много заправок.

Все хранимые поля обязательны. Неизвестный расход представлен отсутствием строки
в `consumptions`; `LEFT JOIN` возвращает `NULL`, и страница показывает «Не указан».
Положительные числовые значения проверяются `CHECK`, названия не могут быть пустыми.
Удаление связанного автомобиля или топлива блокируется внешними ключами.
На каждом соединении включается `PRAGMA foreign_keys = ON`.

`REAL` сохранён для совместимости с исходными JSON и учебной предметной областью;
денежные показатели выводятся с двумя знаками после запятой.

## Файлы SQL-слоя

- `sql/schema.sql` — повторно исполняемая схема с `CREATE TABLE IF NOT EXISTS`.
- `sql/queries.sql` — 12 именованных запросов; это единственный источник SQL для страниц.
- `db/database.py` — абсолютный путь к базе, соединения, `sqlite3.Row`, чтение запросов.
- `db/import_json.py` — импорт четырёх JSON в одной транзакции: автомобили, топливо,
  нормы расхода, заправки. Родительские записи импортируются раньше дочерних.
- `data/fuel_service.sqlite` — созданная база с фактическими данными проекта.

Импорт сохраняет исходные ID. Повторный запуск не создаёт дублей и не меняет строки
с существующими ID (`ON CONFLICT(id) DO NOTHING`). Это первоначальный перенос,
а не синхронизация: для изменения существующих записей нужен отдельный запрос.
При нарушении связей или ограничений вся транзакция откатывается.
Для исходного набора перенесено по одной записи в каждую из четырёх таблиц.

## SQL-запросы и пользовательские сценарии

| № | Имя в queries.sql | Назначение и использование |
| --- | --- | --- |
| 1 | cars | Список автомобилей, SELECT и ORDER BY: `/cars/`, варианты поиска |
| 2 | fuels | Список топлива, SELECT и ORDER BY: `/fuels/`, варианты поиска |
| 3 | car_detail | WHERE и LEFT JOIN: автомобиль и необязательная норма расхода |
| 4 | refuelings | JOIN трёх таблиц: список заправок и вычисление стоимости |
| 5 | refueling_detail | JOIN и WHERE: отдельная заправка |
| 6 | search | WHERE, AND, параметры: автомобиль, топливо, минимальный объём |
| 7 | without_refuelings | NOT EXISTS: автомобили без заправок в статистике |
| 8 | totals | COUNT, SUM, AVG, MIN, MAX: количество, объём и стоимость |
| 9 | consumption_totals | COUNT, AVG: количество норм и средний расход |
| 10 | by_car | LEFT JOIN, GROUP BY: число заправок и расходы по автомобилям |
| 11 | by_fuel | LEFT JOIN, GROUP BY: число заправок и объём по видам топлива |
| 12 | frequent_cars | GROUP BY, HAVING: автомобили с числом заправок больше порога |

Минимум методички соблюдён: 12 запросов, два списка, несколько WHERE и JOIN,
два самостоятельных агрегатных запроса и три запроса с группировкой.
Все результаты используются на веб-страницах.
Поиск свободных помещений из учебного примера адаптирован к предметной области:
пользователь ищет заправки по автомобилю, виду топлива и объёму; отдельно видит
автомобили без заправок. Дата и статус отмены не добавлены, поскольку исходная
модель заправки их не содержит.

Значения передаются отдельно от SQL через `?`. Соединения закрываются после чтения.
`sqlite3.Row` позволяет получать столбцы по имени. Представления передают строки
и подготовленные карточки через `context` в шаблоны Django.

## Страницы

- `/` — главная.
- `/cars/`, `/cars/<id>/` — автомобили и расход.
- `/fuels/` — виды топлива.
- `/refuelings/`, `/refuelings/<id>/` — заправки со связанными данными.
- `/refuelings/search/` — поиск (GET: `car`, `fuel`, `min_liters`).
- `/refuelings/statistics/` — статистика (GET: `threshold`, условие количества `> threshold`).

Например: `/refuelings/search/?car=1&fuel=1&min_liters=20`.
Неизвестные ID карточек возвращают 404. Пустые результаты поиска и статистики
обрабатываются шаблонами; неверные числовые параметры показывают сообщение.
Навигация использует именованные URL.

Общий шаблон — `templates/base.html`, навигация — `templates/includes/navigation.html`.
Карточки вынесены в `cars/templates/cars/includes/car_card.html` и
`refuelings/templates/refuelings/includes/refueling_card.html`.
Статика находится в `homepage/static/homepage/`. Используются DTL, Bootstrap 5.3,
CSS и JavaScript. Формы изменения данных в ПР7 не реализуются.

## Проверки

```powershell
python manage.py check
pytest -v -p no:cacheprovider
flake8 .
```

`tests/test_database.py` проверяет все 12 запросов, импорт без дублей, откат импорта,
внешние ключи, ограничения, агрегаты, страницы, фильтры, пустые результаты и
некорректные параметры. Используется временная база; рабочие данные не меняются.
Остальные тесты проверяют сохранённую консольную реализацию.

Для ручной проверки SQL без установки SQLite CLI:

```powershell
python -c "from db.database import fetch_all; print([dict(row) for row in fetch_all('by_car')])"
python -c "from db.database import fetch_all; print([dict(row) for row in fetch_all('search', (1, 1, 1, 1, 20))])"
```

Запросы с `?` требуют параметров; их нельзя выполнять как единый скрипт без
привязки значений. Автоматические тесты исполняют каждый запрос через `sqlite3`.
SQLite CLI и расширение VS Code для просмотра БД не требуются для запуска.

## Консольная версия

```powershell
python main.py
```

## Фиксация результата

Перед сдачей просмотреть `git diff`, затем сохранить изменения ПР7 коммитом с
префиксом `PR7:`, например `PR7: add SQLite storage, search and statistics`.
Локальные изменения настроек следует проверить отдельно перед включением в коммит.
