class Fuel:
    """Вид топлива."""

    def __init__(
        self,
        fuel_id: int,
        name: str
    ) -> None:
        self.id = fuel_id
        self.name = name

    def __str__(self) -> str:
        return f'{self.id}. {self.name}'


def add_fuel(
    fuels: list[Fuel],
    name: str
) -> Fuel:
    """Добавить вид топлива."""
    fuel = Fuel(
        fuel_id=len(fuels) + 1,
        name=name
    )

    fuels.append(fuel)
    return fuel


def find_fuel_by_id(
    fuels: list[Fuel],
    fuel_id: int
) -> Fuel | None:
    """Найти топливо по ID."""
    for fuel in fuels:
        if fuel.id == fuel_id:
            return fuel

    return None


def find_fuels(
    fuels: list[Fuel],
    query: str
) -> list[Fuel]:
    """Найти топливо по названию."""
    found_fuels = []

    for fuel in fuels:
        if query.lower() in fuel.name.lower():
            found_fuels.append(fuel)

    return found_fuels


def sort_fuels(
    fuels: list[Fuel]
) -> list[Fuel]:
    """Отсортировать виды топлива."""
    return sorted(
        fuels,
        key=lambda fuel: fuel.name
    )
