from django.urls import path
from .views import enter_ride, show_rides, CarShift, show_detail, edit_ride

urlpatterns = [
    path('add/', enter_ride, name="new_ride"),
    path('added/', enter_ride, name="ride_added"),
    path('list/', show_rides, name="rides_all"),
    path('totaldaycar/', CarShift.as_view(), name="total_day_car"),
    path('detail/(?P<number>[0-9]+)/', show_detail, name="ride_detail"),
    path('edit/(?P<number>[0-9]+)/', edit_ride, name="ride_change"),
]