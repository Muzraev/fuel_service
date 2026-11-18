from cars.models import Car


def service_context(request):
    return {'service_title': 'Сервис учёта топлива',
            'service_car_count': Car.objects.count()}
