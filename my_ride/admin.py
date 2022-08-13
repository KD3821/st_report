from django.contrib import admin
from .models import Week, Shift, Car, Driver, Ride, ExtraTax

admin.site.register(Week)
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(ExtraTax)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['date', 'week']
    list_filter = ['week']


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['number', 'car', 'driver', 'price', 'cash', 'save_tax', 'saved_tax_result', 'extra_tax', 'tax_result', 'comment']
    list_filter = ['shift']
