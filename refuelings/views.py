from django.http import HttpResponse


def refuelings(request):
    return HttpResponse(
        'Список заправок'
    )


def refueling_detail(
    request,
    refueling_id
):
    return HttpResponse(
        f'Заправка {refueling_id}'
    )
