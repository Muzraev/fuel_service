from cars import Car


class Trip:
    """Поездка автомобиля."""

    def __init__(
        self,
        trip_id: int,
        car: Car,
        distance_km: float,
        fuel_liters: float
    ) -> None:
        if distance_km <= 0:
            raise ValueError(
                'Расстояние должно быть больше нуля.'
            )

        if fuel_liters < 0:
            raise ValueError(
                'Количество топлива не может быть отрицательным.'
            )

        self.id = trip_id
        self.car = car
        self.distance_km = distance_km
        self.fuel_liters = fuel_liters

    def calculate_consumption(self) -> float:
        """Рассчитать расход топлива на 100 км."""
        return self.fuel_liters / self.distance_km * 100

    def get_consumption_status(self) -> str:
        """Определить уровень расхода топлива."""
        consumption = self.calculate_consumption()

        if consumption <= 7:
            return 'Низкий расход топлива.'
        elif consumption <= 12:
            return 'Нормальный расход топлива.'

        return 'Высокий расход топлива.'

    def __str__(self) -> str:
        consumption = self.calculate_consumption()

        return (
            f'Поездка №{self.id}: {self.car.name}, '
            f'{self.distance_km} км, '
            f'{self.fuel_liters} л, '
            f'{consumption:.2f} л/100 км'
        )


def add_trip(
    trips: list[Trip],
    car: Car,
    distance_km: float,
    fuel_liters: float
) -> Trip:
    """Добавить поездку."""
    trip = Trip(
        trip_id=len(trips) + 1,
        car=car,
        distance_km=distance_km,
        fuel_liters=fuel_liters
    )

    trips.append(trip)
    return trip


def find_trips_by_car(
    trips: list[Trip],
    car: Car
) -> list[Trip]:
    """Найти поездки автомобиля."""
    found_trips = []

    for trip in trips:
        if trip.car.id == car.id:
            found_trips.append(trip)

    return found_trips


def sort_trips_by_consumption(
    trips: list[Trip]
) -> list[Trip]:
    """Отсортировать поездки по расходу."""
    return sorted(
        trips,
        key=lambda trip: trip.calculate_consumption()
    )


def get_average_consumption(
    trips: list[Trip]
) -> float:
    """Рассчитать средний расход топлива."""
    if not trips:
        return 0.0

    total = sum(
        trip.calculate_consumption()
        for trip in trips
    )

    return total / len(trips)
