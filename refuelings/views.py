from django.http import HttpResponse

from homepage.views import page
from storage import (
    load_cars,
    load_fuels,
    load_refuelings
)


CARS_FILE = 'data/cars.json'
FUELS_FILE = 'data/fuels.json'
REFUELINGS_FILE = 'data/refuelings.json'


def get_refuelings():
    """Загрузить данные о заправках."""
    cars = load_cars(CARS_FILE)
    fuels = load_fuels(FUELS_FILE)

    return load_refuelings(
        REFUELINGS_FILE,
        cars,
        fuels
    )


def refuelings(request):
    """Показать список заправок."""
    refuelings_list = get_refuelings()

    if not refuelings_list:
        content = """
            <h1>Заправки</h1>
            <p>Заправок пока нет.</p>
        """

        return HttpResponse(
            page('Заправки', content)
        )

    rows = ''

    total_cost = 0

    for refueling in refuelings_list:
        cost = refueling.calculate_cost()
        total_cost += cost

        rows += f"""
            <tr>
                <td>{refueling.id}</td>
                <td>{refueling.car.name}</td>
                <td>{refueling.fuel.name}</td>
                <td>{refueling.fuel_liters:.1f} л</td>
                <td>{refueling.price_per_liter:.2f} руб.</td>
                <td>{cost:.2f} руб.</td>
                <td>
                    <a href="/refuelings/{refueling.id}/"
                       class="btn btn-sm btn-dark">
                        Подробнее
                    </a>
                </td>
            </tr>
        """

    content = f"""
        <h1>Заправки</h1>

        <p>
            <strong>Общая стоимость:</strong>
            {total_cost:.2f} руб.
        </p>

        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Автомобиль</th>
                    <th>Топливо</th>
                    <th>Количество</th>
                    <th>Цена за литр</th>
                    <th>Стоимость</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>
                {rows}
            </tbody>
        </table>
    """

    return HttpResponse(
        page('Заправки', content)
    )


def refueling_detail(
    request,
    refueling_id
):
    """Показать одну заправку."""
    refuelings_list = get_refuelings()

    refueling = None

    for item in refuelings_list:
        if item.id == refueling_id:
            refueling = item
            break

    if refueling is None:
        return HttpResponse(
            page(
                'Заправка не найдена',
                '<h1>Заправка не найдена</h1>'
            ),
            status=404
        )

    cost = refueling.calculate_cost()

    content = f"""
        <h1>Заправка №{refueling.id}</h1>

        <p>
            <strong>Автомобиль:</strong>
            {refueling.car.name}
        </p>

        <p>
            <strong>Топливо:</strong>
            {refueling.fuel.name}
        </p>

        <p>
            <strong>Количество:</strong>
            {refueling.fuel_liters:.1f} л
        </p>

        <p>
            <strong>Цена за литр:</strong>
            {refueling.price_per_liter:.2f} руб.
        </p>

        <p>
            <strong>Стоимость:</strong>
            {cost:.2f} руб.
        </p>

        <a href="/refuelings/"
           class="btn btn-dark">
            Назад
        </a>
    """

    return HttpResponse(
        page(
            f'Заправка №{refueling.id}',
            content
        )
    )
