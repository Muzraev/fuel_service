from django.db import models


class RefuelingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Refueling.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=Refueling.Status.CANCELLED)

    def completed(self):
        return self.filter(status=Refueling.Status.COMPLETED)

    def for_date(self, date):
        return self.filter(date=date)

    def for_car(self, car):
        return self.filter(car=car)


class Refueling(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Запланирована'
        CANCELLED = 'cancelled', 'Отменена'
        COMPLETED = 'completed', 'Проведена'

    car = models.ForeignKey(
        'cars.Car', on_delete=models.PROTECT, related_name='refuelings',
        verbose_name='Автомобиль')
    fuel = models.ForeignKey(
        'fuels.Fuel', on_delete=models.PROTECT, related_name='refuelings',
        verbose_name='Топливо')
    fuel_liters = models.FloatField('Объём, л')
    price_per_liter = models.FloatField('Цена за литр, руб.')
    date = models.DateField('Дата', null=True, blank=True,
                            help_text='Для старых записей дата неизвестна')
    status = models.CharField('Статус', max_length=12,
                              choices=Status.choices, default=Status.COMPLETED)
    amount = models.GeneratedField(
        expression=models.F('fuel_liters') * models.F('price_per_liter'),
        output_field=models.FloatField(), db_persist=True,
        verbose_name='Стоимость, руб.')
    objects = RefuelingQuerySet.as_manager()

    class Meta:
        ordering = ['id']
        verbose_name = 'Заправка'
        verbose_name_plural = 'Заправки'
        constraints = [
            models.CheckConstraint(condition=models.Q(fuel_liters__gt=0),
                                   name='positive_liters'),
            models.CheckConstraint(condition=models.Q(price_per_liter__gt=0),
                                   name='positive_price'),
            models.CheckConstraint(
                condition=models.Q(status__in=['active', 'cancelled',
                                               'completed']),
                name='valid_refueling_status'),
        ]

    @property
    def total_cost(self):
        return self.fuel_liters * self.price_per_liter

    def __str__(self):
        return f'Заправка №{self.pk}: {self.car}'
