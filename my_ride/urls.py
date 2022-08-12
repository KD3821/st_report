from django.urls import path
from .views import enter_ride, show_rides, CarShift

urlpatterns = [
    path('add/', enter_ride, name="new_ride"),
    path('added/', enter_ride, name="ride_added"),
    path('list/', show_rides, name="rides_all"),
    path('totaldaycar/', CarShift.as_view(), name="total_day_car"),
]