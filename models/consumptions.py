from .cars import Car


class Consumption:
    """Расход топлива автомобиля."""

    def __init__(
        self,
        consumption_id: int,
        car: Car,
        liters_per_100km: float
    ) -> None:
        if liters_per_100km <= 0:
            raise ValueError(
                'Расход топлива должен быть больше нуля.'
            )

        self.id = consumption_id
        self.car = car
        self.liters_per_100km = liters_per_100km

    def calculate_fuel_for_distance(
        self,
        distance_km: float
    ) -> float:
        """Рассчитать количество топлива на расстояние."""
        if distance_km <= 0:
            raise ValueError(
                'Расстояние должно быть больше нуля.'
            )

        return (
            distance_km
            * self.liters_per_100km
            / 100
        )

    def __str__(self) -> str:
        return (
            f'{self.car.name}: '
            f'{self.liters_per_100km:.1f} л/100 км'
        )


def find_consumption_by_car(
    consumptions: list[Consumption],
    car: Car
) -> Consumption | None:
    """Найти расход автомобиля."""
    for consumption in consumptions:
        if consumption.car.id == car.id:
            return consumption

    return None


def add_consumption(
    consumptions: list[Consumption],
    car: Car,
    liters_per_100km: float
) -> Consumption:
    """Добавить или изменить расход автомобиля."""
    existing = find_consumption_by_car(
        consumptions,
        car
    )

    if existing is not None:
        if liters_per_100km <= 0:
            raise ValueError(
                'Расход топлива должен быть больше нуля.'
            )

        existing.liters_per_100km = liters_per_100km
        return existing

    consumption = Consumption(
        consumption_id=len(consumptions) + 1,
        car=car,
        liters_per_100km=liters_per_100km
    )

    consumptions.append(consumption)
    return consumption
