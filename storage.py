import json

from models.cars import Car
from models.consumptions import Consumption
from models.fuels import Fuel
from models.refueling import Refueling


def read_json(filename: str) -> list[dict]:
    """Прочитать JSON-файл."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print(f'Ошибка чтения файла {filename}.')
        return []


def write_json(
    filename: str,
    data: list[dict]
) -> None:
    """Записать данные в JSON-файл."""
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
        cars.append(
            Car(
                car_id=item['id'],
                name=item['name']
            )
        )

    return cars


def save_cars(
    filename: str,
    cars: list[Car]
) -> None:
    """Сохранить автомобили."""
    data = []

    for car in cars:
        data.append({
            'id': car.id,
            'name': car.name
        })

    write_json(filename, data)


def load_fuels(filename: str) -> list[Fuel]:
    """Загрузить виды топлива."""
    data = read_json(filename)
    fuels = []

    for item in data:
        fuels.append(
            Fuel(
                fuel_id=item['id'],
                name=item['name']
            )
        )

    return fuels


def save_fuels(
    filename: str,
    fuels: list[Fuel]
) -> None:
    """Сохранить виды топлива."""
    data = []

    for fuel in fuels:
        data.append({
            'id': fuel.id,
            'name': fuel.name
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


def find_fuel_by_id(
    fuels: list[Fuel],
    fuel_id: int
) -> Fuel | None:
    """Найти топливо по ID."""
    for fuel in fuels:
        if fuel.id == fuel_id:
            return fuel

    return None


def load_consumptions(
    filename: str,
    cars: list[Car]
) -> list[Consumption]:
    """Загрузить данные о расходе."""
    data = read_json(filename)
    consumptions = []

    for item in data:
        car = find_car_by_id(
            cars,
            item['car_id']
        )

        if car is None:
            continue

        consumptions.append(
            Consumption(
                consumption_id=item['id'],
                car=car,
                liters_per_100km=item[
                    'liters_per_100km'
                ]
            )
        )

    return consumptions


def save_consumptions(
    filename: str,
    consumptions: list[Consumption]
) -> None:
    """Сохранить данные о расходе."""
    data = []

    for consumption in consumptions:
        data.append({
            'id': consumption.id,
            'car_id': consumption.car.id,
            'liters_per_100km':
                consumption.liters_per_100km
        })

    write_json(filename, data)


def load_refuelings(
    filename: str,
    cars: list[Car],
    fuels: list[Fuel]
) -> list[Refueling]:
    """Загрузить заправки."""
    data = read_json(filename)
    refuelings = []

    for item in data:
        car = find_car_by_id(
            cars,
            item['car_id']
        )

        fuel = find_fuel_by_id(
            fuels,
            item['fuel_id']
        )

        if car is None or fuel is None:
            continue

        refuelings.append(
            Refueling(
                refueling_id=item['id'],
                car=car,
                fuel=fuel,
                fuel_liters=item['fuel_liters'],
                price_per_liter=item[
                    'price_per_liter'
                ]
            )
        )

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
            'fuel_id': refueling.fuel.id,
            'fuel_liters': refueling.fuel_liters,
            'price_per_liter':
                refueling.price_per_liter
        })

    write_json(filename, data)
