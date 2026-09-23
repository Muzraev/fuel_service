class Car:
    """Автомобиль."""

    def __init__(self, car_id: int, name: str):
        self.id = car_id
        self.name = name

    def __str__(self) -> str:
        return f'{self.id}. {self.name}'


def add_car(cars: list[Car], name: str) -> Car:
    """Добавить автомобиль."""
    car = Car(
        car_id=len(cars) + 1,
        name=name
    )

    cars.append(car)
    return car


def find_cars(cars: list[Car], query: str) -> list[Car]:
    """Найти автомобили по части названия."""
    found_cars = []

    for car in cars:
        if query.lower() in car.name.lower():
            found_cars.append(car)

    return found_cars


def sort_cars(cars: list[Car]) -> list[Car]:
    """Отсортировать автомобили по названию."""
    return sorted(cars, key=lambda car: car.name)
