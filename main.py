from cars import Car, add_car, find_cars, sort_cars
from refueling import (
    Refueling,
    add_refueling,
    find_refuelings_by_car
)
from storage import (
    find_car_by_id,
    load_cars,
    load_refuelings,
    load_trips,
    save_cars,
    save_refuelings,
    save_trips
)
from trips import (
    Trip,
    add_trip,
    find_trips_by_car,
    get_average_consumption,
    sort_trips_by_consumption
)
from utils import input_float, input_int


CARS_FILE = 'data/cars.json'
TRIPS_FILE = 'data/trips.json'
REFUELINGS_FILE = 'data/refuelings.json'


def show_cars(cars: list[Car]) -> None:
    """Показать список автомобилей."""
    if not cars:
        print('Автомобилей пока нет.')
        return

    print('\nАвтомобили:')

    for car in sort_cars(cars):
        print(car)


def show_trips(trips: list[Trip]) -> None:
    """Показать список поездок."""
    if not trips:
        print('Поездок пока нет.')
        return

    print('\nПоездки:')

    for trip in trips:
        print(trip)
        print(f'Статус: {trip.get_consumption_status()}')


def show_refuelings(
    refuelings: list[Refueling]
) -> None:
    """Показать список заправок."""
    if not refuelings:
        print('Заправок пока нет.')
        return

    print('\nЗаправки:')

    for refueling in refuelings:
        print(refueling)


def main() -> None:
    """Запустить сервис учета топлива."""
    cars = load_cars(CARS_FILE)
    trips = load_trips(TRIPS_FILE, cars)
    refuelings = load_refuelings(
        REFUELINGS_FILE,
        cars
    )

    while True:
        print('\n=== Сервис учета топлива ===')
        print('1. Показать автомобили')
        print('2. Добавить автомобиль')
        print('3. Найти автомобиль')
        print('4. Добавить поездку')
        print('5. Показать поездки')
        print('6. Показать поездки автомобиля')
        print('7. Показать средний расход')
        print('8. Отсортировать поездки по расходу')
        print('9. Добавить заправку')
        print('10. Показать заправки')
        print('11. Показать заправки автомобиля')
        print('0. Выход')

        choice = input('Выберите действие: ')

        if choice == '1':
            show_cars(cars)

        elif choice == '2':
            name = input(
                'Введите название автомобиля: '
            ).strip()

            if not name:
                print(
                    'Название автомобиля '
                    'не может быть пустым.'
                )
                continue

            car = add_car(cars, name)
            save_cars(CARS_FILE, cars)

            print(
                f'Автомобиль {car.name} '
                'успешно добавлен.'
            )

        elif choice == '3':
            query = input(
                'Введите название для поиска: '
            )

            found_cars = find_cars(
                cars,
                query
            )

            if not found_cars:
                print('Автомобили не найдены.')
            else:
                for car in found_cars:
                    print(car)

        elif choice == '4':
            if not cars:
                print(
                    'Сначала добавьте автомобиль.'
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
                print(
                    'Автомобиль с таким ID '
                    'не найден.'
                )
                continue

            distance_km = input_float(
                'Введите пройденное расстояние, км: '
            )

            fuel_liters = input_float(
                'Введите количество '
                'потраченного топлива, л: '
            )

            try:
                trip = add_trip(
                    trips,
                    car,
                    distance_km,
                    fuel_liters
                )

                save_trips(
                    TRIPS_FILE,
                    trips
                )

                print('Поездка добавлена.')
                print(
                    f'Расход: '
                    f'{trip.calculate_consumption():.2f} '
                    'л/100 км'
                )
                print(
                    f'Статус: '
                    f'{trip.get_consumption_status()}'
                )

            except ValueError as error:
                print(f'Ошибка: {error}')

        elif choice == '5':
            show_trips(trips)

        elif choice == '6':
            if not cars:
                print('Автомобилей пока нет.')
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
                print(
                    'Автомобиль с таким ID '
                    'не найден.'
                )
                continue

            car_trips = find_trips_by_car(
                trips,
                car
            )

            show_trips(car_trips)

        elif choice == '7':
            average = get_average_consumption(
                trips
            )

            print(
                f'Средний расход топлива: '
                f'{average:.2f} л/100 км'
            )

        elif choice == '8':
            sorted_trips = (
                sort_trips_by_consumption(
                    trips
                )
            )

            show_trips(sorted_trips)

        elif choice == '9':
            if not cars:
                print(
                    'Сначала добавьте автомобиль.'
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
                print(
                    'Автомобиль с таким ID '
                    'не найден.'
                )
                continue

            fuel_liters = input_float(
                'Введите количество топлива, л: '
            )

            price_per_liter = input_float(
                'Введите стоимость одного литра: '
            )

            try:
                refueling = add_refueling(
                    refuelings,
                    car,
                    fuel_liters,
                    price_per_liter
                )

                save_refuelings(
                    REFUELINGS_FILE,
                    refuelings
                )

                print('Заправка добавлена.')
                print(
                    f'Стоимость заправки: '
                    f'{refueling.calculate_cost():.2f} '
                    'руб.'
                )

            except ValueError as error:
                print(f'Ошибка: {error}')

        elif choice == '10':
            show_refuelings(refuelings)

        elif choice == '11':
            if not cars:
                print('Автомобилей пока нет.')
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
                print(
                    'Автомобиль с таким ID '
                    'не найден.'
                )
                continue

            car_refuelings = (
                find_refuelings_by_car(
                    refuelings,
                    car
                )
            )

            show_refuelings(
                car_refuelings
            )

        elif choice == '0':
            save_cars(
                CARS_FILE,
                cars
            )
            save_trips(
                TRIPS_FILE,
                trips
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
