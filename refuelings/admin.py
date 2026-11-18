from django.contrib import admin

from .models import Refueling


@admin.action(description='Отметить выбранные заправки отменёнными')
def cancel_refuelings(modeladmin, request, queryset):
    queryset.update(status=Refueling.Status.CANCELLED)


@admin.register(Refueling)
class RefuelingAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'fuel', 'date', 'status',
                    'fuel_liters', 'price_per_liter', 'amount')
    list_display_links = ('id', 'car')
    list_editable = ('status',)
    search_fields = ('car__name', 'fuel__name')
    list_filter = ('status', 'date', 'fuel', 'car')
    ordering = ('-date', '-id')
    list_per_page = 10
    list_select_related = ('car', 'fuel')
    readonly_fields = ('id', 'amount')
    actions = (cancel_refuelings,)


admin.site.site_header = 'Сервис учёта топлива'
admin.site.site_title = 'Управление сервисом'
admin.site.index_title = 'Администрирование'
