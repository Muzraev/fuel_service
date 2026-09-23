import pytest

from trips import (
    add_trip,
    calculate_consumption,
    calculate_fuel_cost,
    get_average_consumption,
    get_consumption_status
)


def test_calculate_consumption():
    result = calculate_consumption(200, 20)

    assert result == 10


def test_calculate_fuel_cost():
    result = calculate_fuel_cost(30, 65)

    assert result == 1950


def test_consumption_status():
    assert get_consumption_status(6) == 'Низкий расход топлива.'
    assert get_consumption_status(10) == 'Нормальный расход топлива.'
    assert get_consumption_status(15) == 'Высокий расход топлива.'


def test_add_trip():
    trips = []

    trip = add_trip(
        trips,
        car_id=1,
        distance_km=200,
        fuel_liters=20,
        price_per_liter=65
    )

    assert trip['id'] == 1
    assert trip['car_id'] == 1
    assert trip['consumption'] == 10
    assert trip['fuel_cost'] == 1300


def test_add_trip_with_wrong_distance():
    trips = []

    with pytest.raises(ValueError):
        add_trip(
            trips,
            car_id=1,
            distance_km=0,
            fuel_liters=20,
            price_per_liter=65
        )


def test_average_consumption():
    trips = [
        {'consumption': 10},
        {'consumption': 20}
    ]

    result = get_average_consumption(trips)

    assert result == 15