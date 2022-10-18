from django.contrib import admin
from .models import Week, Shift, Car, Driver, Ride, ExtraTax, BalanceDriver, PlanShift

admin.site.register(Week)
admin.site.register(ExtraTax)
admin.site.register(BalanceDriver)
admin.site.register(PlanShift)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['plate', 'user']
    list_filter = ['user']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['user']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['date', 'week']
    list_filter = ['week']


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['number', 'car', 'driver', 'price', 'cash', 'save_tax', 'saved_tax_result', 'extra_tax', 'tax_result', 'tip', 'comment']
    list_filter = ['shift']
