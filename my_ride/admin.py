from django.contrib import admin
from .models import Shift, Car, Driver, Ride

admin.site.register(Shift)
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Ride)
