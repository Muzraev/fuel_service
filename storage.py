import json

from cars import Car
from refueling import Refueling
from trips import Trip


def read_json(filename: str) -> list[dict]:
    """Прочитать данные из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print(f'Ошибка чтения файла {filename}.')
        return []


def write_json(filename: str, data: list[dict]) -> None:
    """Сохранить данные в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_cars(filename: str) -> list[Car]:
    """Загрузить автомобили."""
    data = read_json(filename)
    cars = []

    for item in data:
        car = Car(
            car_id=item['id'],
            name=item['name']
        )
        cars.append(car)

    return cars


def save_cars(filename: str, cars: list[Car]) -> None:
    """Сохранить автомобили."""
    data = []

    for car in cars:
        data.append({
            'id': car.id,
            'name': car.name
        })

    write_json(filename, data)


def find_car_by_id(
    cars: list[Car],
    car_id: int
) -> Car | None:
    """Найти автомобиль по ID."""
    for car in cars:
        if car.id == car_id:
            return car

    return None


def load_trips(
    filename: str,
    cars: list[Car]
) -> list[Trip]:
    """Загрузить поездки."""
    data = read_json(filename)
    trips = []

    for item in data:
        car = find_car_by_id(
            cars,
            item['car_id']
        )

        if car is None:
            continue

        trip = Trip(
            trip_id=item['id'],
            car=car,
            distance_km=item['distance_km'],
            fuel_liters=item['fuel_liters']
        )

        trips.append(trip)

    return trips


def save_trips(filename: str, trips: list[Trip]) -> None:
    """Сохранить поездки."""
    data = []

    for trip in trips:
        data.append({
            'id': trip.id,
            'car_id': trip.car.id,
            'distance_km': trip.distance_km,
            'fuel_liters': trip.fuel_liters
        })

    write_json(filename, data)


def load_refuelings(
    filename: str,
    cars: list[Car]
) -> list[Refueling]:
    """Загрузить заправки."""
    data = read_json(filename)
    refuelings = []

    for item in data:
        car = find_car_by_id(
            cars,
            item['car_id']
        )

        if car is None:
            continue

        refueling = Refueling(
            refueling_id=item['id'],
            car=car,
            fuel_liters=item['fuel_liters'],
            price_per_liter=item['price_per_liter']
        )

        refuelings.append(refueling)

    return refuelings


def save_refuelings(
    filename: str,
    refuelings: list[Refueling]
) -> None:
    """Сохранить заправки."""
    data = []

    for refueling in refuelings:
        data.append({
            'id': refueling.id,
            'car_id': refueling.car.id,
            'fuel_liters': refueling.fuel_liters,
            'price_per_liter': refueling.price_per_liter
        })

    write_json(filename, data)
