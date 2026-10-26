from django.shortcuts import render

from db.database import fetch_all, fetch_one


def cars(request):
    """Показать автомобили из SQLite."""
    return render(request, 'cars/car_list.html', {'cars': fetch_all('cars')})


def car_detail(request, car_id):
    """Получить автомобиль и необязательную норму расхода через JOIN."""
    car = fetch_one('car_detail', (car_id,))
    consumption = (
        car if car is not None and car['liters_per_100km'] is not None
        else None
    )
    return render(
        request, 'cars/car_detail.html',
        {'car': car, 'consumption': consumption},
        status=404 if car is None else 200,
    )
