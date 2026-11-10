from django.db import models


class Refueling(models.Model):
    car = models.ForeignKey(
        'cars.Car', on_delete=models.PROTECT, related_name='refuelings')
    fuel = models.ForeignKey(
        'fuels.Fuel', on_delete=models.PROTECT, related_name='refuelings')
    fuel_liters = models.FloatField()
    price_per_liter = models.FloatField()

    class Meta:
        ordering = ['id']
        constraints = [
            models.CheckConstraint(condition=models.Q(fuel_liters__gt=0),
                                   name='positive_liters'),
            models.CheckConstraint(condition=models.Q(price_per_liter__gt=0),
                                   name='positive_price'),
        ]

    @property
    def total_cost(self):
        return self.fuel_liters * self.price_per_liter
