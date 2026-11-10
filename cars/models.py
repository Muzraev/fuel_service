from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name', 'id']

    def __str__(self):
        return self.name


class Consumption(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.PROTECT, related_name='consumption')
    liters_per_100km = models.FloatField()

    class Meta:
        constraints = [models.CheckConstraint(
            condition=models.Q(liters_per_100km__gt=0),
            name='positive_consumption')]
