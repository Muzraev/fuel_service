from django.shortcuts import render

from models.refueling import get_total_cost
from storage import (
    load_cars,
    load_fuels,
    load_refuelings
)


CARS_FILE = 'data/cars.json'
FUELS_FILE = 'data/fuels.json'
REFUELINGS_FILE = 'data/refuelings.json'


def get_refuelings():
    """Загрузить данные о заправках."""
    cars = load_cars(CARS_FILE)
    fuels = load_fuels(FUELS_FILE)

    return load_refuelings(
        REFUELINGS_FILE,
        cars,
        fuels
    )


def refuelings(request):
    """Показать список заправок."""
    refuelings_list = get_refuelings()
    refueling_items = []

    for refueling in refuelings_list:
        refueling_items.append({
            'refueling': refueling,
            'cost': refueling.calculate_cost(),
        })

    context = {
        'refuelings': refuelings_list,
        'refueling_items': refueling_items,
        'total_cost': get_total_cost(refuelings_list),
    }

    return render(
        request,
        'refuelings/refueling_list.html',
        context
    )


def refueling_detail(request, refueling_id):
    """Показать одну заправку."""
    refuelings_list = get_refuelings()
    refueling = None

    for item in refuelings_list:
        if item.id == refueling_id:
            refueling = item
            break

    context = {
        'refueling': refueling,
        'cost': (
            refueling.calculate_cost()
            if refueling is not None
            else None
        ),
    }

    return render(
        request,
        'refuelings/refueling_detail.html',
        context,
        status=404 if refueling is None else 200
    )
