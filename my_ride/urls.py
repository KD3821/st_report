from django.urls import path
from .views import enter_ride, show_rides, CarDay, CarWeek, DriverDay, DriverWeek, show_detail, edit_ride

urlpatterns = [
    path('add/', enter_ride, name="new_ride"),
    path('added/', enter_ride, name="ride_added"),
    path('list/', show_rides, name="rides_all"),
    path('detail/<str:number>/', show_detail, name="ride_detail"),
    path('edit/<str:number>/', edit_ride, name="ride_change"),
    path('total/<str:name>/<str:shift>/', DriverDay.as_view(), name="total_day_driver"),
    # path('total/<str:name>/<str:shift>/', get_driver_day, name="total_day_driver"),
    path('total/<str:name>/<str:week>/', DriverWeek.as_view(), name="total_week_driver"),
    path('total/<str:car>/<str:shift>/', CarDay.as_view(), name="total_day_car"),
    path('total/<str:car>/<str:week>/', CarWeek.as_view(), name="total_week_car"),

]