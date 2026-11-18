from django.db import models


class Fuel(models.Model):
    name = models.CharField('Название', max_length=200)

    class Meta:
        ordering = ['name', 'id']
        verbose_name = 'Вид топлива'
        verbose_name_plural = 'Виды топлива'

    def __str__(self):
        return self.name
