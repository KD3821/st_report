from django.urls import path
from .views import enter_ride, show_rides, CarShift, DriverWeek, show_detail, edit_ride

urlpatterns = [
    path('add/', enter_ride, name="new_ride"),
    path('added/', enter_ride, name="ride_added"),
    path('list/', show_rides, name="rides_all"),
    path('totaldaycar/<str:car>/', CarShift.as_view(), name="total_day_car"),
    path('totalweekdriver/<str:name>/', DriverWeek.as_view(), name="total_week_driver"),
    path('detail/<int:number>/', show_detail, name="ride_detail"),
    path('edit/<int:number>/', edit_ride, name="ride_change"),
]