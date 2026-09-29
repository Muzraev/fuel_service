import pytest

from models.cars import Car
from models.consumptions import (
    Consumption,
    add_consumption,
    find_consumption_by_car
)


def test_consumption_creation():
    car = Car(1, 'Audi')

    consumption = Consumption(
        1,
        car,
        8.5
    )

    assert consumption.car is car
    assert consumption.liters_per_100km == 8.5


def test_calculate_fuel_for_distance():
    car = Car(1, 'Audi')

    consumption = Consumption(
        1,
        car,
        8.5
    )

    result = (
        consumption
        .calculate_fuel_for_distance(200)
    )

    assert result == 17


def test_wrong_consumption():
    car = Car(1, 'Audi')

    with pytest.raises(ValueError):
        Consumption(
            1,
            car,
            0
        )


def test_add_consumption():
    car = Car(1, 'Audi')
    consumptions = []

    consumption = add_consumption(
        consumptions,
        car,
        10
    )

    assert consumption.car is car
    assert len(consumptions) == 1


def test_find_consumption_by_car():
    car = Car(1, 'Audi')

    consumptions = [
        Consumption(
            1,
            car,
            8.5
        )
    ]

    result = find_consumption_by_car(
        consumptions,
        car
    )

    assert result.liters_per_100km == 8.5
