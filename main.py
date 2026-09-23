from cars import add_car, find_cars, sort_cars
from storage import load_data, save_data
from trips import (
    add_trip,
    find_trips_by_car,
    get_average_consumption,
    get_consumption_status,
    sort_trips_by_consumption
)
from utils import input_float, input_int


CARS_FILE = 'data/cars.json'
TRIPS_FILE = 'data/trips.json'


def show_cars(cars: list[dict]) -> None:
    """Показать список автомобилей."""
    if not cars:
        print('Автомобилей пока нет.')
        return

    print('\nАвтомобили:')

    for car in sort_cars(cars):
        print(f'{car["id"]}. {car["name"]}')


def show_trips(trips: list[dict], cars: list[dict]) -> None:
    """Показать список поездок."""
    if not trips:
        print('Поездок пока нет.')
        return

    print('\nПоездки:')

    for trip in trips:
        car_name = 'Неизвестный автомобиль'

        for car in cars:
            if car['id'] == trip['car_id']:
                car_name = car['name']
                break

        status = get_consumption_status(trip['consumption'])

        print(
            f'Поездка №{trip["id"]}: '
            f'{car_name}, '
            f'{trip["distance_km"]} км, '
            f'{trip["fuel_liters"]} л, '
            f'{trip["consumption"]:.2f} л/100 км, '
            f'{trip["fuel_cost"]:.2f} руб. '
            f'({status})'
        )


def main() -> None:
    """Запустить сервис учета топлива."""
    cars = load_data(CARS_FILE)
    trips = load_data(TRIPS_FILE)

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
        print('0. Выход')

        choice = input('Выберите действие: ')

        if choice == '1':
            show_cars(cars)

        elif choice == '2':
            name = input('Введите название автомобиля: ').strip()

            if not name:
                print('Название автомобиля не может быть пустым.')
                continue

            car = add_car(cars, name)
            save_data(CARS_FILE, cars)

            print(
                f'Автомобиль {car["name"]} '
                'успешно добавлен.'
            )

        elif choice == '3':
            query = input('Введите название для поиска: ')
            found_cars = find_cars(cars, query)

            if not found_cars:
                print('Автомобили не найдены.')
            else:
                for car in found_cars:
                    print(f'{car["id"]}. {car["name"]}')

        elif choice == '4':
            if not cars:
                print('Сначала добавьте автомобиль.')
                continue

            show_cars(cars)

            car_id = input_int('Введите ID автомобиля: ')

            car_exists = False

            for car in cars:
                if car['id'] == car_id:
                    car_exists = True
                    break

            if not car_exists:
                print('Автомобиль с таким ID не найден.')
                continue

            distance_km = input_float(
                'Введите пройденное расстояние, км: '
            )
            fuel_liters = input_float(
                'Введите количество топлива, л: '
            )
            price_per_liter = input_float(
                'Введите стоимость одного литра: '
            )

            try:
                trip = add_trip(
                    trips,
                    car_id,
                    distance_km,
                    fuel_liters,
                    price_per_liter
                )

                save_data(TRIPS_FILE, trips)

                print('Поездка добавлена.')
                print(
                    f'Расход: '
                    f'{trip["consumption"]:.2f} л/100 км'
                )
                print(
                    f'Стоимость топлива: '
                    f'{trip["fuel_cost"]:.2f} руб.'
                )

            except ValueError as error:
                print(f'Ошибка: {error}')

        elif choice == '5':
            show_trips(trips, cars)

        elif choice == '6':
            car_id = input_int('Введите ID автомобиля: ')
            car_trips = find_trips_by_car(trips, car_id)

            show_trips(car_trips, cars)

        elif choice == '7':
            average = get_average_consumption(trips)

            print(
                f'Средний расход топлива: '
                f'{average:.2f} л/100 км'
            )

        elif choice == '8':
            sorted_trips = sort_trips_by_consumption(trips)
            show_trips(sorted_trips, cars)

        elif choice == '0':
            print('Работа программы завершена.')
            break

        else:
            print('Такого пункта меню нет.')


if __name__ == '__main__':
    main()