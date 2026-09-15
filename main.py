from datetime import date


def calculate_consumption(distance_km, fuel_liters):
    """Рассчитывает расход топлива на 100 км."""
    return fuel_liters / distance_km * 100


def calculate_fuel_cost(fuel_liters, price_per_liter):
    """Рассчитывает стоимость потраченного топлива."""
    return fuel_liters * price_per_liter


def get_consumption_status(consumption):
    """Возвращает оценку расхода топлива."""
    if consumption <= 7:
        return 'Низкий расход топлива.'
    elif consumption <= 12:
        return 'Нормальный расход топлива.'
    else:
        return 'Высокий расход топлива.'


print('Сервис учета топлива')
print('--------------------')

car_name = input('Введите название автомобиля: ')

distance_km = float(
    input('Введите пройденное расстояние, км: ').replace(',', '.')
)

fuel_liters = float(
    input('Введите количество потраченного топлива, л: ').replace(',', '.')
)

price_per_liter = float(
    input('Введите стоимость одного литра топлива: ').replace(',', '.')
)

if distance_km <= 0:
    print('Расстояние должно быть больше нуля.')
elif fuel_liters < 0 or price_per_liter < 0:
    print('Количество топлива и стоимость не могут быть отрицательными.')
else:
    consumption = calculate_consumption(distance_km, fuel_liters)
    fuel_cost = calculate_fuel_cost(fuel_liters, price_per_liter)
    status = get_consumption_status(consumption)

    current_date = date.today()

    print()
    print('Отчет о поездке')
    print('---------------')
    print(f'Дата: {current_date}')
    print(f'Автомобиль: {car_name}')
    print(f'Расстояние: {distance_km:.1f} км')
    print(f'Потрачено топлива: {fuel_liters:.1f} л')
    print(f'Расход: {consumption:.2f} л/100 км')
    print(f'Стоимость топлива: {fuel_cost:.2f} руб.')
    print(f'Оценка: {status}')