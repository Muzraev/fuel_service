from django.http import HttpResponse


def fuels(request):
    return HttpResponse(
        'Виды топлива'
    )
