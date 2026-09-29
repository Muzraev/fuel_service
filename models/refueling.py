from .cars import Car
from .fuels import Fuel


class Refueling:
    """Заправка автомобиля."""

    def __init__(
        self,
        refueling_id: int,
        car: Car,
        fuel: Fuel,
        fuel_liters: float,
        price_per_liter: float
    ) -> None:
        if fuel_liters <= 0:
            raise ValueError(
                'Количество топлива должно быть больше нуля.'
            )

        if price_per_liter <= 0:
            raise ValueError(
                'Цена топлива должна быть больше нуля.'
            )

        self.id = refueling_id
        self.car = car
        self.fuel = fuel
        self.fuel_liters = fuel_liters
        self.price_per_liter = price_per_liter

    def calculate_cost(self) -> float:
        """Рассчитать стоимость заправки."""
        return self.fuel_liters * self.price_per_liter

    def __str__(self) -> str:
        return (
            f'Заправка №{self.id}: '
            f'{self.car.name}, '
            f'{self.fuel.name}, '
            f'{self.fuel_liters:.1f} л, '
            f'{self.calculate_cost():.2f} руб.'
        )


def add_refueling(
    refuelings: list[Refueling],
    car: Car,
    fuel: Fuel,
    fuel_liters: float,
    price_per_liter: float
) -> Refueling:
    """Добавить заправку."""
    refueling = Refueling(
        refueling_id=len(refuelings) + 1,
        car=car,
        fuel=fuel,
        fuel_liters=fuel_liters,
        price_per_liter=price_per_liter
    )

    refuelings.append(refueling)
    return refueling


def find_refuelings_by_car(
    refuelings: list[Refueling],
    car: Car
) -> list[Refueling]:
    """Найти заправки автомобиля."""
    found_refuelings = []

    for refueling in refuelings:
        if refueling.car.id == car.id:
            found_refuelings.append(refueling)

    return found_refuelings


def find_refuelings_by_fuel(
    refuelings: list[Refueling],
    fuel: Fuel
) -> list[Refueling]:
    """Найти заправки по виду топлива."""
    found_refuelings = []

    for refueling in refuelings:
        if refueling.fuel.id == fuel.id:
            found_refuelings.append(refueling)

    return found_refuelings


def sort_refuelings_by_cost(
    refuelings: list[Refueling]
) -> list[Refueling]:
    """Отсортировать заправки по стоимости."""
    return sorted(
        refuelings,
        key=lambda refueling: refueling.calculate_cost()
    )


def get_total_cost(
    refuelings: list[Refueling]
) -> float:
    """Рассчитать общую стоимость всех заправок."""
    return sum(
        refueling.calculate_cost()
        for refueling in refuelings
    )
