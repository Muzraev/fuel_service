"""ORM integration checks use an isolated temporary SQLite database."""
import os
import tempfile
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuel_service_web.settings')
import django  # noqa: E402
django.setup()
from django.core.management import call_command  # noqa: E402
from django.db import connection  # noqa: E402
from django.db.models.deletion import ProtectedError  # noqa: E402
from django.test import Client, override_settings  # noqa: E402
from cars.models import Car  # noqa: E402
from fuels.models import Fuel  # noqa: E402
from refuelings.models import Refueling  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture
def orm_db():
    previous = connection.settings_dict['NAME']
    connection.close()
    with tempfile.TemporaryDirectory() as folder:
        connection.settings_dict['NAME'] = str(Path(folder) / 'test.sqlite')
        try:
            call_command('migrate', verbosity=0)
            call_command('import_pr7', verbosity=0)
            with override_settings(ALLOWED_HOSTS=['testserver']):
                yield Client()
        finally:
            connection.close()
            connection.settings_dict['NAME'] = previous


def test_pages_and_invalid_parameters(orm_db):
    for url in ('/', '/cars/', '/cars/1/', '/fuels/', '/refuelings/',
                '/refuelings/1/', '/refuelings/search/',
                '/refuelings/statistics/'):
        assert orm_db.get(url).status_code == 200, url
    for url in ('/cars/999999/', '/refuelings/999999/'):
        assert orm_db.get(url).status_code == 404
    for value in ('abc', 'nan', 'inf', '-1'):
        response = orm_db.get('/refuelings/search/', {'min_liters': value})
        assert 'Проверьте параметры' in response.content.decode()
    assert 'Порог должен быть' in orm_db.get(
        '/refuelings/statistics/?threshold=abc').content.decode()


def test_filter_sort_pagination_and_empty_parent(orm_db):
    car = Car.objects.create(name='Demo empty')
    assert 'Не указан' in orm_db.get(f'/cars/{car.pk}/').content.decode()
    assert 'Demo empty' in orm_db.get(
        '/refuelings/statistics/').content.decode()
    fuel = Fuel.objects.first()
    for n in range(12):
        Refueling.objects.create(car=car, fuel=fuel, fuel_liters=n + 1,
                                 price_per_liter=60)
    url = f'/refuelings/search/?car={car.pk}&sort=id&min_liters=2'
    html = orm_db.get(url).content.decode()
    assert 'из 3' in html
    assert 'page=2' in html and 'sort=id' in html
    assert f'car={car.pk}' in html and 'min_liters=2' in html
    assert orm_db.get(url + '&page=bad').status_code == 200
    assert orm_db.get(url + '&page=999').status_code == 200
    assert orm_db.get(url + '&sort=unknown').status_code == 200
    assert 'заправок не найдено' in orm_db.get(
        url + '&min_liters=99999').content.decode()
    with pytest.raises(ProtectedError):
        car.delete()
    assert car.refuelings.count() == 12


def test_import_repeat_conflict_and_crud(orm_db):
    before = Refueling.objects.count()
    call_command('import_pr7', verbosity=0)
    assert Refueling.objects.count() == before
    car = Car.objects.create(name='Demo')
    car.name = 'Changed'
    car.save()
    assert Car.objects.get(pk=car.pk).name == 'Changed'
    pk = car.pk
    car.delete()
    assert not Car.objects.filter(pk=pk).exists()
    from django.core.management.base import CommandError
    original = Car.objects.get(pk=1)
    original.name = 'Conflict'
    original.save()
    with pytest.raises(CommandError):
        call_command('import_pr7', verbosity=0)
    assert Car.objects.get(pk=1).name == 'Conflict'
