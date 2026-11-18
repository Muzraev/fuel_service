# Сервис учёта топлива — ПР9

Индивидуальный проект: Музраев Санджи Мингиянович, ЭФБО-16-24.
Автомобили, топливо, нормы расхода и заправки. Консольная JSON-версия
и SQL-реализация ПР7 сохранены; прежнее описание — README_PR7.md.

## Запуск (терминал VS Code, PowerShell, из корня проекта)

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py import_pr7
.\.venv\Scripts\python.exe manage.py runserver --insecure
```

Если окружения ещё нет: `python -m venv .venv`, затем
`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
Главная: http://127.0.0.1:8000/.
DEBUG=False сохранён; --insecure служит только для локальной статики.

## Модели и перенос

- cars/models.py: Car(name), Consumption(car, liters_per_100km).
- fuels/models.py: Fuel(name).
- refuelings/models.py: Refueling(car, fuel, fuel_liters, price_per_liter).
- Неявные PK — BigAutoField. Названия CharField(200), числа FloatField
  для совместимости с REAL ПР7; стоимость выводится с двумя знаками.
- Все поля обязательны (blank=False, null=False); числовые CHECK > 0.
- Car → Consumption: один к одному, необязательность выражена отсутствием
  нормы. Car/Fuel → Refueling: один ко многим. PROTECT запрещает удалять
  используемые автомобиль/топливо. related_name: consumption/refuelings.

Стратегия: новые управляемые Django таблицы в db.sqlite3. Предметная база
data/fuel_service.sqlite остаётся источником ПР7 и открывается только на чтение.
Служебные таблицы Django сохраняются. Не применяем --fake к старой схеме.
Команда import_pr7 сохраняет ID, переносит родителей перед дочерними записями
в одной транзакции, выполняет full_clean. Совпадающие записи пропускаются,
конфликт существующего ID отменяет всю транзакцию. Повторный запуск безопасен.
Это перенос, а не двусторонняя синхронизация; JSON-консоль остаётся независимой.
Резервные копии исходной базы и файлов сделаны отдельно перед обновлением.

## Страницы и ORM

Сохранены /, /cars/, /cars/<id>/, /fuels/, /refuelings/,
/refuelings/<id>/, /refuelings/search/, /refuelings/statistics/.
GET поиска: car, fuel, min_liters, q (название автомобиля ИЛИ топлива),
exclude_fuel; sort: id, -id, cost, -cost, car, liters; page.
Сортировка по умолчанию -cost, затем id. Неизвестный sort получает этот
вариант. Фильтры применяются перед сортировкой и Paginator(5).
querystring сохраняет параметры при смене страницы. Неверная страница
обрабатывается get_page; неверные числовые фильтры показывают сообщение.
Список и поиск используют один общий обработчик listing.

Отдельные ORM-выборки и их назначение (не подсчёт вызовов в одной цепочке):

1. Car.objects.all() — список автомобилей.
2. Car.filter(name__icontains=q) — поиск автомобиля.
3. Car.select_related('consumption') + get_object_or_404 — карточка.
4. Fuel.order_by('name', 'id') — список топлива.
5. costs() — стоимость через annotate и F.
6. rows.filter(car_id=...) — отбор заправок автомобиля.
7. rows.filter(fuel_id=...) — отбор вида топлива (совместим с №6).
8. rows.filter(fuel_liters__gte=...) — отбор объёма.
9. rows.filter(Q(car__name__icontains=q) | Q(fuel__name__icontains=q)) — поиск.
10. rows.exclude(fuel_id=...) — исключение топлива.
11. rows.order_by(*SORTS[...]) — разрешённая сортировка, включая связи.
12. rows.aggregate(Sum('cost')) — сумма отфильтрованного набора.
13. rows.values(..., car_name=F('car__name'), fuel_name=F('fuel__name')) — карточки.
14. Refueling.select_related('car', 'fuel') + get_object_or_404 — подробности.
15. costs().aggregate(Count, Sum, Avg, Min, Max) — общая статистика.
16. Consumption.aggregate(Count, Avg) — статистика расхода.
17. Car.annotate(Count, Sum).order_by('-total_cost', 'id') — группы автомобилей.
18. Fuel.annotate(Count, Sum) — группы топлива.
19. Car.filter(refuelings__isnull=True) — автомобили без заправок.
20. by_car.filter(count__gt=threshold) — условие на агрегат (HAVING).
21. Paginator(values, PAGE_SIZE).get_page(...) — ограниченная выборка страницы.

Создание, изменение, удаление выполняются через ORM в Django Shell;
формы записи не добавлялись в рамках ПР9. Тесты показывают CRUD и PROTECT.
В представлениях нет прямого SQL. values возвращает словари с именами связей,
шаблоны карточек сохранены. Детальная страница использует объект модели.
Отсутствующая карточка возвращает 404. LEFT JOIN в статистике сохраняет
родителей без дочерних записей; суммы пустых групп равны 0.

## Проверки

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pytest -v -p no:cacheprovider
.\.venv\Scripts\python.exe -m flake8 .
```

tests/test_database.py проверяет сохранённый SQL-слой.
tests/test_orm.py использует отдельную временную базу: миграции, перенос,
повторный перенос и конфликт, CRUD, PROTECT, страницы, 404, пустые родители,
фильтры, сортировку, пагинацию и сохранение GET-параметров.
