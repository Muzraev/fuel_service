from django.http import HttpResponse


def cars(request):
    return HttpResponse(
        'Список автомобилей'
    )


def car_detail(request, car_id):
    return HttpResponse(
        f'Автомобиль {car_id}'
    )
