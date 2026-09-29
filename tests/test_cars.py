from models.cars import (
    Car,
    add_car,
    find_car_by_id
)


def test_car_creation():
    car = Car(1, 'Audi A6')

    assert car.id == 1
    assert car.name == 'Audi A6'


def test_car_str():
    car = Car(1, 'Audi A6')

    assert str(car) == '1. Audi A6'


def test_add_car():
    cars = []

    car = add_car(
        cars,
        'BMW X5'
    )

    assert car.id == 1
    assert len(cars) == 1


def test_find_car_by_id():
    cars = [
        Car(1, 'Audi'),
        Car(2, 'BMW')
    ]

    result = find_car_by_id(
        cars,
        2
    )

    assert result.name == 'BMW'
