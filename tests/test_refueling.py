import pytest

from cars import Car
from refueling import (
    Refueling,
    add_refueling,
    find_refuelings_by_car
)


def test_refueling_creation():
    car = Car(1, 'Audi')

    refueling = Refueling(
        refueling_id=1,
        car=car,
        fuel_liters=30,
        price_per_liter=65
    )

    assert refueling.id == 1
    assert refueling.car is car
    assert refueling.fuel_liters == 30
    assert refueling.price_per_liter == 65


def test_calculate_cost():
    car = Car(1, 'Audi')
    refueling = Refueling(1, car, 30, 65)

    assert refueling.calculate_cost() == 1950


def test_add_refueling():
    car = Car(1, 'Audi')
    refuelings = []

    refueling = add_refueling(
        refuelings,
        car,
        30,
        65
    )

    assert refueling.id == 1
    assert refueling.car is car
    assert len(refuelings) == 1


def test_wrong_fuel_liters():
    car = Car(1, 'Audi')

    with pytest.raises(ValueError):
        Refueling(
            refueling_id=1,
            car=car,
            fuel_liters=0,
            price_per_liter=65
        )


def test_find_refuelings_by_car():
    audi = Car(1, 'Audi')
    bmw = Car(2, 'BMW')

    refuelings = [
        Refueling(1, audi, 30, 65),
        Refueling(2, bmw, 40, 60)
    ]

    result = find_refuelings_by_car(
        refuelings,
        audi
    )

    assert len(result) == 1
    assert result[0].car is audi
