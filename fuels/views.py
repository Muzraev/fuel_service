from django.shortcuts import render

from .models import Fuel


def fuels(request):
    return render(request, 'fuels/fuel_list.html', {
        'fuels': Fuel.objects.order_by('name', 'id')})
