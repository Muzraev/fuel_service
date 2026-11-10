import math

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, render

from cars.models import Car, Consumption
from fuels.models import Fuel
from .models import Refueling


SORTS = {'id': ('id',), '-id': ('-id',),
         'cost': ('cost', 'id'), '-cost': ('-cost', 'id'),
         'car': ('car__name', 'id'), 'liters': ('fuel_liters', 'id')}
PAGE_SIZE = 5


def costs():
    return Refueling.objects.annotate(
        cost=F('fuel_liters') * F('price_per_liter'))


def filtered(request):
    rows = costs()
    for key in ('car', 'fuel'):
        if request.GET.get(key):
            value = int(request.GET[key])
            if not 0 < value <= 2**63 - 1:
                raise ValueError
            rows = rows.filter(**{key + '_id': value})
    liters = float(request.GET.get('min_liters') or 0)
    if not math.isfinite(liters) or liters < 0:
        raise ValueError
    rows = rows.filter(fuel_liters__gte=liters)
    q = request.GET.get('q', '').strip()
    if q:
        rows = rows.filter(Q(car__name__icontains=q)
                           | Q(fuel__name__icontains=q))
    if request.GET.get('exclude_fuel'):
        excluded = int(request.GET['exclude_fuel'])
        if not 0 < excluded <= 2**63 - 1:
            raise ValueError
        rows = rows.exclude(fuel_id=excluded)
    sort = request.GET.get('sort', '-cost')
    return rows.order_by(*SORTS.get(sort, SORTS['-cost']))


def listing(request, template):
    context = {'cars': Car.objects.all(), 'fuels': Fuel.objects.all()}
    try:
        rows = filtered(request)
    except (ValueError, OverflowError):
        context['error'] = 'Проверьте параметры: объём должен быть от 0.'
        rows = costs().none()
    context['total_cost'] = rows.aggregate(value=Sum('cost'))['value'] or 0
    # values() retrieves related names in SQL; no model N+1 queries.
    values = rows.values('id', 'car_id', 'fuel_id', 'fuel_liters',
                         'price_per_liter', 'cost', car_name=F('car__name'),
                         fuel_name=F('fuel__name'))
    page = Paginator(values, PAGE_SIZE).get_page(request.GET.get('page'))
    items = []
    for row in page:
        row['car'] = {'id': row['car_id'], 'name': row['car_name']}
        row['fuel'] = {'id': row['fuel_id'], 'name': row['fuel_name']}
        items.append({'refueling': row, 'cost': row['cost']})
    context.update(page_obj=page, refuelings=page,
                   refueling_items=items)
    return render(request, template, context)


def refuelings(request):
    return listing(request, 'refuelings/refueling_list.html')


def search(request):
    return listing(request, 'refuelings/search.html')


def refueling_detail(request, refueling_id):
    row = get_object_or_404(
        Refueling.objects.select_related('car', 'fuel'), pk=refueling_id)
    return render(request, 'refuelings/refueling_detail.html', {
        'refueling': row, 'cost': row.total_cost})


def statistics(request):
    by_car = Car.objects.annotate(
        count=Count('refuelings'),
        total_cost=Sum(F('refuelings__fuel_liters')
                       * F('refuelings__price_per_liter'), default=0),
    ).order_by('-total_cost', 'id')
    context = {
        'totals': costs().aggregate(
            count=Count('id'), total_liters=Sum('fuel_liters', default=0),
            total_cost=Sum('cost', default=0), average_cost=Avg('cost'),
            min_cost=Min('cost'), max_cost=Max('cost')),
        'consumption': Consumption.objects.aggregate(
            count=Count('id'), average_consumption=Avg('liters_per_100km')),
        'by_car': by_car,
        'by_fuel': Fuel.objects.annotate(
            count=Count('refuelings'),
            total_liters=Sum('refuelings__fuel_liters', default=0)),
        'without_refuelings': Car.objects.filter(refuelings__isnull=True),
    }
    try:
        threshold = int(request.GET.get('threshold') or 0)
        if not 0 <= threshold <= 2**63 - 1:
            raise ValueError
    except ValueError:
        context['error'] = 'Порог должен быть целым числом от 0.'
    else:
        context['frequent_cars'] = by_car.filter(count__gt=threshold)
    return render(request, 'refuelings/statistics.html', context)
