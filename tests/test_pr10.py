"""Admin, permissions, new schema and QuerySet integration scenarios."""
from datetime import date
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError, connection, transaction
from django.test.utils import CaptureQueriesContext

from cars.models import Car
from refuelings.models import Refueling
from test_orm import orm_db  # noqa: F401


def test_slug_generated_value_status_and_date(orm_db):  # noqa: F811
    car = Car.objects.first()
    assert orm_db.get(car.get_absolute_url()).status_code == 200
    assert orm_db.get('/cars/by-slug/missing/').status_code == 404
    row = Refueling.objects.first()
    row.fuel_liters = 12
    row.price_per_liter = 70
    row.date = date(2026, 11, 18)
    row.status = Refueling.Status.ACTIVE
    row.save()
    row.refresh_from_db()
    assert row.amount == 840
    assert Refueling.objects.active().for_date(row.date).count() == 1
    assert Refueling.objects.completed().count() == 0
    html = orm_db.get('/refuelings/').content.decode()
    assert f'Заправка №{row.pk}' not in html
    html = orm_db.get('/refuelings/search/?status=active').content.decode()
    assert f'Заправка №{row.pk}' in html
    row.status = Refueling.Status.CANCELLED
    row.save()
    assert Refueling.objects.cancelled().count() == 1
    assert 'Отменено: 1' in orm_db.get(
        '/refuelings/statistics/').content.decode()
    assert 'Проверьте параметры' in orm_db.get(
        '/refuelings/search/?date=bad').content.decode()
    assert 'Проверьте параметры' in orm_db.get(
        '/refuelings/search/?status=bad').content.decode()


def test_admin_crud_search_inline_and_permissions(orm_db):  # noqa: F811
    user = get_user_model().objects.create_superuser(
        'admin', '', 'Test-pass1!')
    orm_db.force_login(user)
    for url in ('/admin/', '/admin/cars/car/', '/admin/fuels/fuel/',
                '/admin/refuelings/refueling/?q=Audi&status__exact=completed'):
        assert orm_db.get(url).status_code == 200
    car = Car.objects.first()
    assert 'id_refuelings-TOTAL_FORMS' in orm_db.get(
        f'/admin/cars/car/{car.pk}/change/').content.decode()
    response = orm_db.post('/admin/fuels/fuel/add/',
                           {'name': 'Admin fuel', '_save': 'Save',
                            'refuelings-TOTAL_FORMS': '0',
                            'refuelings-INITIAL_FORMS': '0'})
    assert response.status_code == 302
    group = Group.objects.create(name='Наблюдатели')
    group.permissions.add(Permission.objects.get(
        codename='view_car', content_type__app_label='cars'))
    staff = get_user_model().objects.create_user('viewer', is_staff=True)
    staff.groups.add(group)
    orm_db.force_login(staff)
    assert orm_db.get('/admin/cars/car/').status_code == 200
    assert orm_db.get('/admin/cars/car/add/').status_code == 403
    assert orm_db.get('/admin/refuelings/refueling/').status_code == 403


def test_related_query_budget_context_and_database_error(orm_db):  # noqa: F811
    with CaptureQueriesContext(connection) as queries:
        rows = list(Refueling.objects.select_related('car', 'fuel'))
        assert rows
        for row in rows:
            assert row.car.name and row.fuel.name
    assert len(queries) == 1
    assert 'Автомобилей:' in orm_db.get('/').content.decode()
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Refueling.objects.filter(pk=rows[0].pk).update(fuel_liters=0)
    assert Refueling.objects.get(pk=rows[0].pk).fuel_liters > 0
    with patch('refuelings.views.filtered', side_effect=ValueError):
        assert 'Проверьте параметры' in orm_db.get(
            '/refuelings/search/').content.decode()


def test_cancelled_plan_does_not_block_car(orm_db):  # noqa: F811
    row = Refueling.objects.first()
    row.status = Refueling.Status.ACTIVE
    row.date = date(2026, 11, 18)
    row.save()
    url = '/cars/without-plans/?date=2026-11-18'
    assert row.car.name not in orm_db.get(url).content.decode()
    row.status = Refueling.Status.CANCELLED
    row.save()
    assert row.car.name in orm_db.get(url).content.decode()
    assert 'Укажите корректную дату' in orm_db.get(
        '/cars/without-plans/?date=wrong').content.decode()
