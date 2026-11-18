import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Car(models.Model):
    name = models.CharField('Название', max_length=200,
                            help_text='Марка и модель автомобиля')
    slug = models.SlugField('Адрес', unique=True, max_length=220, blank=True)

    class Meta:
        ordering = ['name', 'id']
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (slugify(self.name) or 'car') + '-'
            self.slug += uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cars:car_by_slug', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Consumption(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.PROTECT, related_name='consumption',
        verbose_name='Автомобиль')
    liters_per_100km = models.FloatField('Расход, л/100 км')

    class Meta:
        verbose_name = 'Норма расхода'
        verbose_name_plural = 'Нормы расхода'
        constraints = [models.CheckConstraint(
            condition=models.Q(liters_per_100km__gt=0),
            name='positive_consumption')]

    def __str__(self):
        return f'{self.car}: {self.liters_per_100km} л/100 км'
