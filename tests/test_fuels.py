from models.fuels import (
    Fuel,
    add_fuel,
    find_fuel_by_id
)


def test_fuel_creation():
    fuel = Fuel(1, 'АИ-95')

    assert fuel.id == 1
    assert fuel.name == 'АИ-95'


def test_fuel_str():
    fuel = Fuel(1, 'АИ-95')

    assert str(fuel) == '1. АИ-95'


def test_add_fuel():
    fuels = []

    fuel = add_fuel(
        fuels,
        'Дизель'
    )

    assert fuel.id == 1
    assert len(fuels) == 1


def test_find_fuel_by_id():
    fuels = [
        Fuel(1, 'АИ-95'),
        Fuel(2, 'АИ-98')
    ]

    result = find_fuel_by_id(
        fuels,
        2
    )

    assert result.name == 'АИ-98'
