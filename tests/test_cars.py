from cars import add_car, find_cars, sort_cars


def test_add_car():
    cars = []

    car = add_car(cars, 'Audi')

    assert car['id'] == 1
    assert car['name'] == 'Audi'
    assert len(cars) == 1


def test_find_cars():
    cars = [
        {'id': 1, 'name': 'Audi A6'},
        {'id': 2, 'name': 'BMW X5'}
    ]

    result = find_cars(cars, 'audi')

    assert len(result) == 1
    assert result[0]['name'] == 'Audi A6'


def test_sort_cars():
    cars = [
        {'id': 1, 'name': 'BMW'},
        {'id': 2, 'name': 'Audi'}
    ]

    result = sort_cars(cars)

    assert result[0]['name'] == 'Audi'
    assert result[1]['name'] == 'BMW'