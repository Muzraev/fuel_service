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


def car_by_slug(request, slug):
    car = get_object_or_404(
        Car.objects.select_related('consumption'), slug=slug)
    return render(request, 'cars/car_detail.html', {
        'car': car, 'consumption': getattr(car, 'consumption', None),
    })


def without_plans(request):
    from datetime import date
    from refuelings.models import Refueling
    rows = Car.objects.none()
    error = None
    selected = request.GET.get('date', '')
    if selected:
        try:
            day = date.fromisoformat(selected)
        except ValueError:
            error = 'Укажите корректную дату.'
        else:
            planned = Refueling.objects.active().for_date(day).values_list(
                'car_id', flat=True)
            rows = Car.objects.exclude(pk__in=planned)
    return render(request, 'cars/without_plans.html', {
        'cars': rows, 'error': error, 'selected_date': selected})
