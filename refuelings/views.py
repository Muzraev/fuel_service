import math

from django.shortcuts import render

from db.database import fetch_all, fetch_one


def as_item(row):
    """Подготовить результат JOIN для существующей карточки заправки."""
    refueling = dict(row)
    refueling['car'] = {'id': row['car_id'], 'name': row['car_name']}
    refueling['fuel'] = {'id': row['fuel_id'], 'name': row['fuel_name']}
    return {'refueling': refueling, 'cost': row['cost']}


def refuelings(request):
    """Показать заправки и общую стоимость из базы данных."""
    rows = fetch_all('refuelings')
    return render(request, 'refuelings/refueling_list.html', {
        'refuelings': rows,
        'refueling_items': [as_item(row) for row in rows],
        'total_cost': fetch_one('totals')['total_cost'],
    })


def refueling_detail(request, refueling_id):
    """Получить заправку вместе с автомобилем и топливом."""
    row = fetch_one('refueling_detail', (refueling_id,))
    return render(
        request, 'refuelings/refueling_detail.html',
        as_item(row) if row is not None else {},
        status=404 if row is None else 200,
    )


def search(request):
    """Поиск заправок по пользовательским параметрам."""
    context = {'cars': fetch_all('cars'), 'fuels': fetch_all('fuels')}
    try:
        car = int(request.GET['car']) if request.GET.get('car') else None
        fuel = int(request.GET['fuel']) if request.GET.get('fuel') else None
        liters = float(request.GET.get('min_liters') or 0)
        if (not math.isfinite(liters) or liters < 0
                or (car is not None and not 0 < car <= 2**63 - 1)
                or (fuel is not None and not 0 < fuel <= 2**63 - 1)):
            raise ValueError
    except (ValueError, OverflowError):
        context['error'] = 'Проверьте параметры: объём должен быть от 0.'
    else:
        rows = fetch_all('search', (car, car, fuel, fuel, liters))
        context['refueling_items'] = [as_item(row) for row in rows]
    return render(request, 'refuelings/search.html', context)


def statistics(request):
    """Общие показатели, группировка и фильтрация групп в SQL."""
    context = {
        'totals': fetch_one('totals'),
        'consumption': fetch_one('consumption_totals'),
        'by_car': fetch_all('by_car'),
        'by_fuel': fetch_all('by_fuel'),
        'without_refuelings': fetch_all('without_refuelings'),
    }
    try:
        threshold = int(request.GET.get('threshold') or 0)
        if not 0 <= threshold <= 2**63 - 1:
            raise ValueError
    except ValueError:
        context['error'] = 'Порог должен быть целым числом от 0.'
    else:
        context['frequent_cars'] = fetch_all('frequent_cars', (threshold,))
    return render(request, 'refuelings/statistics.html', context)
