from django.shortcuts import render

from models.consumptions import find_consumption_by_car
from storage import (
    find_car_by_id,
    load_cars,
    load_consumptions
)


CARS_FILE = 'data/cars.json'
CONSUMPTIONS_FILE = 'data/consumptions.json'


def cars(request):
    """Показать список автомобилей."""
    cars_list = load_cars(CARS_FILE)

    context = {
        'cars': cars_list,
    }

    return render(
        request,
        'cars/car_list.html',
        context
    )


def car_detail(request, car_id):
    """Показать информацию об автомобиле."""
    cars_list = load_cars(CARS_FILE)
    car = find_car_by_id(
        cars_list,
        car_id
    )

    consumption = None

    if car is not None:
        consumptions = load_consumptions(
            CONSUMPTIONS_FILE,
            cars_list
        )
        consumption = find_consumption_by_car(
            consumptions,
            car
        )

    context = {
        'car': car,
        'consumption': consumption,
    }

    return render(
        request,
        'cars/car_detail.html',
        context,
        status=404 if car is None else 200
    )
