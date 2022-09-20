from django.urls import path
from .views import enter_ride, delete_ride, show_rides, add_plan, show_plan, x_plan, edit_plan, show_weeks, show_week_reports,CarDay, DriverDay, show_detail, edit_ride, DriverWeek, CarWeek, add_report, edit_report, signup

urlpatterns = [
    path('add/', enter_ride, name="new_ride"),
    path('added/', enter_ride, name="ride_added"),
    path('list/', show_rides, name="rides_all"),
    path('start/', show_weeks, name="start"),
    path('week_reports/<str:week>/', show_week_reports, name="week_reports"),
    path('detail/<str:number>/<str:name>/', show_detail, name="ride_detail"),
    path('edit/<str:number>/<str:name>/', edit_ride, name="ride_change"),
    path('delete/<str:number>', delete_ride, name="x_ride"),
    path('totaldd/<str:name>/<str:shift>/', DriverDay.as_view(), name="total_day_driver"),
    path('totalwd/<str:name>/<str:week>/', DriverWeek.as_view(), name="total_week_driver"),
    path('totaldc/<str:car>/<str:shift>/', CarDay.as_view(), name="total_day_car"),
    path('totalwc/<str:car>/<str:week>/', CarWeek.as_view(), name="total_week_car"),
    path('report/<str:shift>/<str:name>/', add_report, name="new_report"),
    path('report/<str:shift>/<str:name>/edit/', edit_report, name="report_change"),
    path('reported/', add_report, name="report_added"),
    path('<str:week>/add_plan/', add_plan, name="plan"),
    path('planned/', add_plan, name="plan_done"),
    path('planlist/<str:week>/', show_plan, name="plan_all"),
    path('xplan/<str:name>/<str:shift>/', x_plan, name="del_plan"),
    path('<str:week>/edit_plan/<str:name>/<str:shift>/', edit_plan, name="plan_change"),
]