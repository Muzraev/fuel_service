def add_car(cars: list[dict], name: str) -> dict:
    """Добавить автомобиль в список."""
    car = {
        'id': len(cars) + 1,
        'name': name
    }

    cars.append(car)
    return car


def find_cars(cars: list[dict], query: str) -> list[dict]:
    """Найти автомобили по части названия."""
    found_cars = []

    for car in cars:
        if query.lower() in car['name'].lower():
            found_cars.append(car)

    return found_cars


def sort_cars(cars: list[dict]) -> list[dict]:
    """Отсортировать автомобили по названию."""
    return sorted(cars, key=lambda car: car['name'])