# Сервис учёта топлива — ПР10

Индивидуальный проект Музраева Санджи Мингияновича, ЭФБО-16-24.
Продолжение ПР9: Django Admin, QuerySet, статусы, slug, GeneratedField,
контекстный процессор и анализ SQL. Предыдущие описания: README_PR9.md,
README_PR7.md. Предметная область — автомобили и заправки, а не Roomly.

## Установка и запуск в PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py import_pr7
python manage.py createsuperuser
$env:DJANGO_DEBUG="1"
python manage.py runserver
```

Если окружение и база уже подготовлены, повторно создавать их не нужно.
Админка: http://127.0.0.1:8000/admin/. Пароль задаётся локально и не хранится
в репозитории. `DJANGO_DEBUG=1` включает Toolbar только для локальной разработки;
без переменной DEBUG=False, локальную статику можно запустить через --insecure.
FUEL_SERVICE_DB позволяет указать отдельную SQLite-базу для демонстрации.
Рабочие записи не заменяются демонстрационными.

## Административная панель

Зарегистрированы Car, Consumption, Fuel и Refueling. Настроены русские названия
приложений, моделей и полей, __str__, help_text, поиск, фильтры, ordering,
list_display_links, list_per_page=10. В Car показаны inline нормы расхода и
заправок; в Fuel — inline заправок. amount и id доступны только для чтения.
RefuelingAdmin загружает car и fuel через list_select_related, ищет по их
названиям, позволяет менять статус в списке и массово отменять выбранные записи.
На рабочем компьютере создана группа «Наблюдатели учёта топлива» только с правами
просмотра. Для другого окружения группу можно создать через /admin/auth/group/.
Права Django не отменяют PROTECT и ограничения модели; конфликты бронирования
не относятся к предметной области этого проекта.

## Модели и миграции

Car.slug — уникальный англоязычный slug; для существующих автомобилей миграция
RunPython присваивает car-ID. Для новых — ASCII slug имени с уникальным суффиксом.
get_absolute_url использует reverse. Новый адрес /cars/by-slug/<slug>/;
старый /cars/<id>/ сохранён. Slug сначала добавляется nullable, заполняется,
затем получает NOT NULL и UNIQUE: миграции cars 0002–0004.

Refueling.Status (TextChoices): active — «Запланирована», cancelled — «Отменена»,
completed — «Проведена». Исходная модель ПР9 не содержала is_cancelled, поэтому
искусственное промежуточное поле не вводилось. AddField с default=completed
сохраняет прежние записи как проведённые. Миграция refuelings 0002 добавляет
также nullable date (неизвестные исторические даты не выдумываются) и amount.
GeneratedField amount хранит произведение объёма и цены, db_persist=True;
после изменения исходных полей его пересчитывает SQLite.

RefuelingQuerySet подключён через as_manager: active(), cancelled(), completed(),
for_date(date), for_car(car). Метод for_date выбирает только известную дату.
После изменений моделей: python manage.py makemigrations; python manage.py migrate.
Для проверки: python manage.py makemigrations --check --dry-run.

## Страницы и бизнес-правила

Сохранены все страницы ПР9. /refuelings/search/ поддерживает car, fuel,
min_liters, q, exclude_fuel, sort, page, а также date=YYYY-MM-DD и status.
По умолчанию показаны проведённые заправки; status=all показывает все.
Отбор, сортировка по разрешённому словарю и Paginator(5) выполняются до
материализации списка; querystring сохраняет параметры.

/refuelings/statistics/ показывает число записей по всем статусам через
условные Count/Q; объём и расходы рассчитываются только по проведённым.
Запланированная или отменённая заправка не должна увеличивать фактические расходы.

/cars/without-plans/?date=2026-11-18 показывает автомобили без запланированной
заправки на дату: active().for_date(...).values_list и exclude(pk__in=...).
Отменённая и проведённая записи не исключают автомобиль. Это адаптация примера
свободных помещений; несколько заправок автомобиля на дату не запрещены.

homepage.context_processors.service_context передаёт название и число автомобилей
в общую навигацию. Это один дополнительный COUNT на рендер страницы.

## Проверки и анализ SQL

```powershell
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
pytest -v -p no:cacheprovider
flake8 .
```

Проверено 30 тестов и 12 subtests. tests/test_pr10.py проверяет Admin и права
просмотра, inline, CRUD, статусы/дату, GeneratedField, slug/404, отсутствие N+1,
контекстный процессор, CHECK/IntegrityError и исключение отменённых планов.
Все тесты БД работают во временной базе, рабочие данные не меняются.

Фактический анализ Debug Toolbar на демонстрационной копии базы: карточка
заправки — 2 SQL (JOIN заправки/автомобиля/топлива и COUNT контекстного процессора),
поиск с пагинацией — 6 SQL (итоговая сумма, COUNT пагинации, текущая страница,
списки автомобилей/топлива и общий COUNT), статистика — 8 SQL.
Запросы связанных объектов не повторяются для каждой карточки.
Числа могут изменяться при добавлении общих компонентов или авторизации.

Личные шпаргалки, доступы к админке, отчёт, резервные и демонстрационные базы
хранятся вне репозитория. В коммит не включаются локальные изменения баз данных.
