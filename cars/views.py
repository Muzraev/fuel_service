from django.shortcuts import get_object_or_404, render

from .models import Car


def cars(request):
    rows = Car.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        rows = rows.filter(name__icontains=q)
    return render(request, 'cars/car_list.html', {'cars': rows})


def car_detail(request, car_id):
    car = get_object_or_404(Car.objects.select_related('consumption'),
                            pk=car_id)
    return render(request, 'cars/car_detail.html', {
        'car': car, 'consumption': getattr(car, 'consumption', None),
    })
