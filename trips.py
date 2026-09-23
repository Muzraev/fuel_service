def calculate_consumption(
    distance_km: float,
    fuel_liters: float
) -> float:
    """Рассчитать расход топлива на 100 км."""
    return fuel_liters / distance_km * 100


def calculate_fuel_cost(
    fuel_liters: float,
    price_per_liter: float
) -> float:
    """Рассчитать стоимость потраченного топлива."""
    return fuel_liters * price_per_liter


def get_consumption_status(consumption: float) -> str:
    """Определить уровень расхода топлива."""
    if consumption <= 7:
        return 'Низкий расход топлива.'
    elif consumption <= 12:
        return 'Нормальный расход топлива.'
    return 'Высокий расход топлива.'


def add_trip(
    trips: list[dict],
    car_id: int,
    distance_km: float,
    fuel_liters: float,
    price_per_liter: float
) -> dict:
    """Добавить поездку в список."""
    if distance_km <= 0:
        raise ValueError('Расстояние должно быть больше нуля.')

    if fuel_liters < 0 or price_per_liter < 0:
        raise ValueError(
            'Количество топлива и стоимость не могут быть отрицательными.'
        )

    consumption = calculate_consumption(distance_km, fuel_liters)
    fuel_cost = calculate_fuel_cost(fuel_liters, price_per_liter)

    trip = {
        'id': len(trips) + 1,
        'car_id': car_id,
        'distance_km': distance_km,
        'fuel_liters': fuel_liters,
        'price_per_liter': price_per_liter,
        'consumption': consumption,
        'fuel_cost': fuel_cost
    }

    trips.append(trip)
    return trip


def find_trips_by_car(
    trips: list[dict],
    car_id: int
) -> list[dict]:
    """Найти поездки определенного автомобиля."""
    found_trips = []

    for trip in trips:
        if trip['car_id'] == car_id:
            found_trips.append(trip)

    return found_trips


def sort_trips_by_consumption(
    trips: list[dict]
) -> list[dict]:
    """Отсортировать поездки по расходу топлива."""
    return sorted(
        trips,
        key=lambda trip: trip['consumption']
    )


def get_average_consumption(trips: list[dict]) -> float:
    """Рассчитать средний расход топлива."""
    if not trips:
        return 0.0

    total = sum(
        trip['consumption']
        for trip in trips
    )

    return total / len(trips)