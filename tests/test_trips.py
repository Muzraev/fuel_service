import pytest

from cars import Car
from trips import (
    Trip,
    add_trip,
    find_trips_by_car,
    get_average_consumption,
    sort_trips_by_consumption
)


def test_trip_creation():
    car = Car(1, 'Audi')

    trip = Trip(
        trip_id=1,
        car=car,
        distance_km=200,
        fuel_liters=20
    )

    assert trip.id == 1
    assert trip.car is car
    assert trip.distance_km == 200
    assert trip.fuel_liters == 20


def test_calculate_consumption():
    car = Car(1, 'Audi')
    trip = Trip(1, car, 200, 20)

    assert trip.calculate_consumption() == 10


def test_consumption_status():
    car = Car(1, 'Audi')

    low = Trip(1, car, 100, 6)
    normal = Trip(2, car, 100, 10)
    high = Trip(3, car, 100, 15)

    assert low.get_consumption_status() == (
        'Низкий расход топлива.'
    )
    assert normal.get_consumption_status() == (
        'Нормальный расход топлива.'
    )
    assert high.get_consumption_status() == (
        'Высокий расход топлива.'
    )


def test_add_trip():
    car = Car(1, 'Audi')
    trips = []

    trip = add_trip(
        trips,
        car,
        200,
        20
    )

    assert trip.id == 1
    assert trip.car is car
    assert len(trips) == 1


def test_wrong_distance():
    car = Car(1, 'Audi')

    with pytest.raises(ValueError):
        Trip(
            trip_id=1,
            car=car,
            distance_km=0,
            fuel_liters=20
        )


def test_find_trips_by_car():
    audi = Car(1, 'Audi')
    bmw = Car(2, 'BMW')

    trips = [
        Trip(1, audi, 100, 10),
        Trip(2, bmw, 200, 20)
    ]

    result = find_trips_by_car(
        trips,
        audi
    )

    assert len(result) == 1
    assert result[0].car is audi


def test_average_consumption():
    car = Car(1, 'Audi')

    trips = [
        Trip(1, car, 100, 10),
        Trip(2, car, 100, 20)
    ]

    assert get_average_consumption(trips) == 15


def test_sort_trips():
    car = Car(1, 'Audi')

    trips = [
        Trip(1, car, 100, 20),
        Trip(2, car, 100, 10)
    ]

    result = sort_trips_by_consumption(trips)

    assert result[0].calculate_consumption() == 10
    assert result[1].calculate_consumption() == 20
