from django.db import models


class Fuel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name', 'id']

    def __str__(self):
        return self.name
