from cars import Car


class Refueling:
    """Заправка автомобиля."""

    def __init__(
        self,
        refueling_id: int,
        car: Car,
        fuel_liters: float,
        price_per_liter: float
    ) -> None:
        if fuel_liters <= 0:
            raise ValueError(
                'Количество топлива должно быть больше нуля.'
            )

        if price_per_liter < 0:
            raise ValueError(
                'Стоимость топлива не может быть отрицательной.'
            )

        self.id = refueling_id
        self.car = car
        self.fuel_liters = fuel_liters
        self.price_per_liter = price_per_liter

    def calculate_cost(self) -> float:
        """Рассчитать стоимость заправки."""
        return self.fuel_liters * self.price_per_liter

    def __str__(self) -> str:
        return (
            f'Заправка №{self.id}: {self.car.name}, '
            f'{self.fuel_liters} л, '
            f'{self.price_per_liter:.2f} руб./л, '
            f'{self.calculate_cost():.2f} руб.'
        )
