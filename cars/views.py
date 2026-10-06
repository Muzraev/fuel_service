from django.http import HttpResponse

from homepage.views import page
from models.consumptions import find_consumption_by_car
from storage import (
    find_car_by_id,
    load_cars,
    load_consumptions
)


CARS_FILE = 'data/cars.json'
CONSUMPTIONS_FILE = 'data/consumptions.json'


def cars(request):
    """Показать список автомобилей."""
    cars_list = load_cars(CARS_FILE)

    if not cars_list:
        content = """
            <h1>Автомобили</h1>
            <p>Автомобилей пока нет.</p>
        """

        return HttpResponse(
            page('Автомобили', content)
        )

    rows = ''

    for car in cars_list:
        rows += f"""
            <tr>
                <td>{car.id}</td>
                <td>{car.name}</td>
                <td>
                    <a href="/cars/{car.id}/"
                       class="btn btn-sm btn-dark">
                        Подробнее
                    </a>
                </td>
            </tr>
        """

    content = f"""
        <h1>Автомобили</h1>

        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Автомобиль</th>
                    <th>Действие</th>
                </tr>
            </thead>

            <tbody>
                {rows}
            </tbody>
        </table>
    """

    return HttpResponse(
        page('Автомобили', content)
    )


def car_detail(request, car_id):
    """Показать информацию об автомобиле."""
    cars_list = load_cars(CARS_FILE)

    car = find_car_by_id(
        cars_list,
        car_id
    )

    if car is None:
        return HttpResponse(
            page(
                'Автомобиль не найден',
                '<h1>Автомобиль не найден</h1>'
            ),
            status=404
        )

    consumptions = load_consumptions(
        CONSUMPTIONS_FILE,
        cars_list
    )

    consumption = find_consumption_by_car(
        consumptions,
        car
    )

    if consumption is None:
        consumption_text = 'Не указан'
    else:
        consumption_text = (
            f'{consumption.liters_per_100km:.1f} '
            'л/100 км'
        )

    content = f"""
        <h1>{car.name}</h1>

        <p>
            <strong>ID автомобиля:</strong>
            {car.id}
        </p>

        <p>
            <strong>Расход топлива:</strong>
            {consumption_text}
        </p>

        <a href="/cars/"
           class="btn btn-dark">
            Назад
        </a>
    """

    return HttpResponse(
        page(car.name, content)
    )
