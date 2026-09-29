import pytest

from models.cars import Car
from models.fuels import Fuel
from models.refueling import (
    Refueling,
    add_refueling,
    find_refuelings_by_car,
    get_total_cost
)


def test_refueling_creation():
    car = Car(1, 'Audi')
    fuel = Fuel(1, 'АИ-95')

    refueling = Refueling(
        1,
        car,
        fuel,
        40,
        65
    )

    assert refueling.car is car
    assert refueling.fuel is fuel
    assert refueling.fuel_liters == 40


def test_calculate_cost():
    car = Car(1, 'Audi')
    fuel = Fuel(1, 'АИ-95')

    refueling = Refueling(
        1,
        car,
        fuel,
        40,
        65
    )

    assert refueling.calculate_cost() == 2600


def test_add_refueling():
    car = Car(1, 'Audi')
    fuel = Fuel(1, 'АИ-95')
    refuelings = []

    refueling = add_refueling(
        refuelings,
        car,
        fuel,
        40,
        65
    )

    assert refueling.id == 1
    assert len(refuelings) == 1


def test_find_refuelings_by_car():
    audi = Car(1, 'Audi')
    bmw = Car(2, 'BMW')
    fuel = Fuel(1, 'АИ-95')

    refuelings = [
        Refueling(
            1,
            audi,
            fuel,
            40,
            65
        ),
        Refueling(
            2,
            bmw,
            fuel,
            30,
            65
        )
    ]

    result = find_refuelings_by_car(
        refuelings,
        audi
    )

    assert len(result) == 1
    assert result[0].car is audi


def test_total_cost():
    car = Car(1, 'Audi')
    fuel = Fuel(1, 'АИ-95')

    refuelings = [
        Refueling(
            1,
            car,
            fuel,
            10,
            60
        ),
        Refueling(
            2,
            car,
            fuel,
            20,
            60
        )
    ]

    assert get_total_cost(refuelings) == 1800


def test_wrong_refueling():
    car = Car(1, 'Audi')
    fuel = Fuel(1, 'АИ-95')

    with pytest.raises(ValueError):
        Refueling(
            1,
            car,
            fuel,
            0,
            65
        )
