from cars import Car, add_car, find_cars, sort_cars


def test_car_creation():
    car = Car(1, 'Audi A6')

    assert car.id == 1
    assert car.name == 'Audi A6'


def test_car_str():
    car = Car(1, 'Audi A6')

    assert str(car) == '1. Audi A6'


def test_add_car():
    cars = []

    car = add_car(cars, 'BMW X5')

    assert car.id == 1
    assert car.name == 'BMW X5'
    assert len(cars) == 1


def test_find_cars():
    cars = [
        Car(1, 'Audi A6'),
        Car(2, 'BMW X5')
    ]

    result = find_cars(cars, 'audi')

    assert len(result) == 1
    assert result[0].name == 'Audi A6'


def test_sort_cars():
    cars = [
        Car(1, 'BMW'),
        Car(2, 'Audi')
    ]

    result = sort_cars(cars)

    assert result[0].name == 'Audi'
    assert result[1].name == 'BMW'
