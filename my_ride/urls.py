from django.urls import path
from .views import enter_ride, delete_ride, show_rides, show_reports, show_weeks, show_week_reports,CarDay, DriverDay, show_detail, edit_ride, DriverWeek, CarWeek, add_report

urlpatterns = [
    path('add/', enter_ride, name="new_ride"),
    path('added/', enter_ride, name="ride_added"),
    path('list/', show_rides, name="rides_all"),
    path('start/', show_weeks, name="start"),
    path('week_reports/<str:week>/', show_week_reports, name="week_reports"),
    path('new_reports/', show_reports, name="new_reports_all"),
    path('detail/<str:number>/', show_detail, name="ride_detail"),
    path('edit/<str:number>/', edit_ride, name="ride_change"),
    path('delete/<str:number>', delete_ride, name="x_ride"),
    path('totaldd/<str:name>/<str:shift>/', DriverDay.as_view(), name="total_day_driver"),
    path('totalwd/<str:name>/<str:week>/', DriverWeek.as_view(), name="total_week_driver"),
    path('totaldc/<str:car>/<str:shift>/', CarDay.as_view(), name="total_day_car"),
    path('totalwc/<str:car>/<str:week>/', CarWeek.as_view(), name="total_week_car"),
    path('report/<str:shift>/<str:name>/', add_report, name="new_report"),
    path('reported/', add_report, name="report_added"),
]