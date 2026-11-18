from django.contrib import admin

from cars.admin import RefuelingInline
from .models import Fuel


class FuelRefuelingInline(RefuelingInline):
    fields = ('car', 'date', 'status', 'fuel_liters',
              'price_per_liter', 'amount')


@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name', 'id')
    list_per_page = 10
    inlines = (FuelRefuelingInline,)
