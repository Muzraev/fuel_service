from models.cars import (
    Car,
    add_car,
    sort_cars
)
from models.consumptions import (
    add_consumption,
    find_consumption_by_car
)
from models.fuels import (
    Fuel,
    add_fuel,
    sort_fuels
)
from models.refueling import (
    Refueling,
    add_refueling,
    find_refuelings_by_car,
    get_total_cost,
    sort_refuelings_by_cost
)
from storage import (
    find_car_by_id,
    find_fuel_by_id,
    load_cars,
    load_consumptions,
    load_fuels,
    load_refuelings,
    save_cars,
    save_consumptions,
    save_fuels,
    save_refuelings
)
from utils import input_float, input_int


CARS_FILE = 'data/cars.json'
FUELS_FILE = 'data/fuels.json'
CONSUMPTIONS_FILE = 'data/consumptions.json'
REFUELINGS_FILE = 'data/refuelings.json'


def show_cars(cars: list[Car]) -> None:
    """Показать автомобили."""
    if not cars:
        print('Автомобилей пока нет.')
        return

    print('\nАвтомобили:')

    for car in sort_cars(cars):
        print(car)


def show_fuels(fuels: list[Fuel]) -> None:
    """Показать виды топлива."""
    if not fuels:
        print('Видов топлива пока нет.')
        return

    print('\nТопливо:')

    for fuel in sort_fuels(fuels):
        print(fuel)


def show_refuelings(
    refuelings: list[Refueling]
) -> None:
    """Показать заправки."""
    if not refuelings:
        print('Заправок пока нет.')
        return

    print('\nЗаправки:')

    for refueling in refuelings:
        print(refueling)


def main() -> None:
    """Запустить сервис учета топлива."""
    cars = load_cars(CARS_FILE)
    fuels = load_fuels(FUELS_FILE)

    consumptions = load_consumptions(
        CONSUMPTIONS_FILE,
        cars
    )

    refuelings = load_refuelings(
        REFUELINGS_FILE,
        cars,
        fuels
    )

    while True:
        print('\n=== Сервис учета топлива ===')
        print('1. Добавить заправку')
        print('2. Показать все заправки')
        print('3. Показать заправки автомобиля')
        print('4. Общая стоимость заправок')
        print('5. Сортировать заправки по стоимости')
        print('6. Добавить автомобиль')
        print('7. Показать автомобили')
        print('8. Добавить вид топлива')
        print('9. Показать виды топлива')
        print('10. Указать расход автомобиля')
        print('11. Показать расход автомобиля')
        print('12. Рассчитать топливо на расстояние')
        print('0. Выход')

        choice = input('Выберите действие: ')

        if choice == '1':
            if not cars:
                print(
                    'Сначала добавьте автомобиль.'
                )
                continue

            if not fuels:
                print(
                    'Сначала добавьте вид топлива.'
                )
                continue

            show_cars(cars)

            car_id = input_int(
                'Введите ID автомобиля: '
            )

            car = find_car_by_id(
                cars,
                car_id
            )

            if car is None:
                print('Автомобиль не найден.')
                continue

            show_fuels(fuels)

            fuel_id = input_int(
                'Введите ID топлива: '
            )

            fuel = find_fuel_by_id(
                fuels,
                fuel_id
            )

            if fuel is None:
                print('Топливо не найдено.')
                continue

            fuel_liters = input_float(
                'Количество топлива, л: '
            )

            price_per_liter = input_float(
                'Цена за литр, руб.: '
            )

            try:
                refueling = add_refueling(
                    refuelings,
                    car,
                    fuel,
                    fuel_liters,
                    price_per_liter
                )

                save_refuelings(
                    REFUELINGS_FILE,
                    refuelings
                )

                print('Заправка добавлена.')
                print(
                    f'Стоимость: '
                    f'{refueling.calculate_cost():.2f} руб.'
                )

            except ValueError as error:
                print(f'Ошибка: {error}')

        elif choice == '2':
            show_refuelings(refuelings)

        elif choice == '3':
            show_cars(cars)

            car_id = input_int(
                'Введите ID автомобиля: '
            )

            car = find_car_by_id(
                cars,
                car_id
            )

            if car is None:
                print('Автомобиль не найден.')
                continue

            result = find_refuelings_by_car(
                refuelings,
                car
            )

            show_refuelings(result)

        elif choice == '4':
            total = get_total_cost(
                refuelings
            )

            print(
                f'Общая стоимость заправок: '
                f'{total:.2f} руб.'
            )

        elif choice == '5':
            result = sort_refuelings_by_cost(
                refuelings
            )

            show_refuelings(result)

        elif choice == '6':
            name = input(
                'Введите название автомобиля: '
            ).strip()

            if not name:
                print(
                    'Название не может быть пустым.'
                )
                continue

            car = add_car(
                cars,
                name
            )

            save_cars(
                CARS_FILE,
                cars
            )

            print(
                f'Автомобиль {car.name} добавлен.'
            )

        elif choice == '7':
            show_cars(cars)

        elif choice == '8':
            name = input(
                'Введите название топлива: '
            ).strip()

            if not name:
                print(
                    'Название не может быть пустым.'
                )
                continue

            fuel = add_fuel(
                fuels,
                name
            )

            save_fuels(
                FUELS_FILE,
                fuels
            )

            print(
                f'Топливо {fuel.name} добавлено.'
            )

        elif choice == '9':
            show_fuels(fuels)

        elif choice == '10':
            show_cars(cars)

            car_id = input_int(
                'Введите ID автомобиля: '
            )

            car = find_car_by_id(
                cars,
                car_id
            )

            if car is None:
                print('Автомобиль не найден.')
                continue

            value = input_float(
                'Введите расход, л/100 км: '
            )

            try:
                consumption = add_consumption(
                    consumptions,
                    car,
                    value
                )

                save_consumptions(
                    CONSUMPTIONS_FILE,
                    consumptions
                )

                print(
                    f'Расход для {car.name}: '
                    f'{consumption.liters_per_100km:.1f} '
                    'л/100 км'
                )

            except ValueError as error:
                print(f'Ошибка: {error}')

        elif choice == '11':
            show_cars(cars)

            car_id = input_int(
                'Введите ID автомобиля: '
            )

            car = find_car_by_id(
                cars,
                car_id
            )

            if car is None:
                print('Автомобиль не найден.')
                continue

            consumption = find_consumption_by_car(
                consumptions,
                car
            )

            if consumption is None:
                print(
                    'Расход для автомобиля '
                    'не указан.'
                )
            else:
                print(consumption)

        elif choice == '12':
            show_cars(cars)

            car_id = input_int(
                'Введите ID автомобиля: '
            )

            car = find_car_by_id(
                cars,
                car_id
            )

            if car is None:
                print('Автомобиль не найден.')
                continue

            consumption = find_consumption_by_car(
                consumptions,
                car
            )

            if consumption is None:
                print(
                    'Сначала укажите расход '
                    'автомобиля.'
                )
                continue

            distance = input_float(
                'Введите расстояние, км: '
            )

            try:
                fuel_needed = (
                    consumption
                    .calculate_fuel_for_distance(
                        distance
                    )
                )

                print(
                    f'Потребуется топлива: '
                    f'{fuel_needed:.2f} л'
                )

            except ValueError as error:
                print(f'Ошибка: {error}')

        elif choice == '0':
            save_cars(
                CARS_FILE,
                cars
            )
            save_fuels(
                FUELS_FILE,
                fuels
            )
            save_consumptions(
                CONSUMPTIONS_FILE,
                consumptions
            )
            save_refuelings(
                REFUELINGS_FILE,
                refuelings
            )

            print(
                'Работа программы завершена.'
            )
            break

        else:
            print('Такого пункта меню нет.')


if __name__ == '__main__':
    main()
