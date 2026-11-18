from django.contrib import admin

from refuelings.models import Refueling
from .models import Car, Consumption


class RefuelingInline(admin.TabularInline):
    model = Refueling
    extra = 0
    fields = ('fuel', 'date', 'status', 'fuel_liters',
              'price_per_liter', 'amount')
    readonly_fields = ('amount',)
    show_change_link = True


class ConsumptionInline(admin.StackedInline):
    model = Consumption
    extra = 0


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name', 'id')
    list_per_page = 10
    readonly_fields = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ConsumptionInline, RefuelingInline)


@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ('car', 'liters_per_100km')
    search_fields = ('car__name',)
    list_select_related = ('car',)
