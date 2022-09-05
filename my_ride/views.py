from django.shortcuts import render
from django.views import View
from .forms import RideForm, TotalDayDriverForm, TotalDayCarForm, ReportDriverForm
from .models import Ride, Week, Shift, BalanceDriver
from django.contrib import messages
from total import GrossDay, SaveTax, TaxRide
from accounting import DriverDayBalance


def prettify(rides):
    for ride in rides:
        if ride.cash == False:
            ride.cash = '---'
        else:
            ride.cash = ride.price
        if ride.save_tax == False:
            ride.save_tax = '---'
        else:
            ride.save_tax = ride.saved_tax_result
        if ride.tax_result == 0:
            ride.tax_result = '--'
        if ride.toll == 0:
            ride.toll = '---'
        if ride.tip == 0:
            ride.tip = '---'
    return rides



def enter_ride(request):
    ride = Ride()
    form = RideForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        ride.number = data.get('number')
        ride.driver = data.get('driver')
        ride.car = data.get('car')
        ride.shift = data.get('shift')
        ride.price = data.get('price')
        ride.tip = data.get('tip')
        ride.cash = data.get('cash')
        ride.toll = data.get('toll')
        ride.save_tax = data.get('save_tax')
        if ride.save_tax == True:
            tax = SaveTax()
            ride.saved_tax_result = tax.tax_saved(ride.price)
        ride.extra_tax = data.get('extra_tax')
        calc_tax = TaxRide()
        ride.tax_result = calc_tax.tax_used(ride.price, ride.extra_tax)
        ride.comment = data.get('comment')
        ride.save()
        messages.success(request, 'Поездка добавлена!')
        return render(request, 'ride_done.html', {'ride': ride})
    return render(request, 'add_ride.html', {'form': form})



def edit_ride(request, number):
    ride = Ride.objects.get(number=number)
    form = RideForm(request.POST or None, initial={
        'number': ride.number,
        'car': ride.car,
        'driver': ride.driver,
        'shift': ride.shift,
        'price': ride.price,
        'tip': ride.tip,
        'cash': ride.cash,
        'toll': ride.toll,
        'save_tax': ride.save_tax,
        'extra_tax': ride.extra_tax,
        'comment': ride.comment
    })
    if form.is_valid():
        data = form.cleaned_data
        ride.number = data.get('number')
        ride.driver = data.get('driver')
        ride.car = data.get('car')
        ride.shift = data.get('shift')
        ride.price = data.get('price')
        ride.tip = data.get('tip')
        ride.cash = data.get('cash')
        ride.toll = data.get('toll')
        ride.save_tax = data.get('save_tax')
        if ride.save_tax == True:
            tax = SaveTax()
            ride.saved_tax_result = tax.tax_saved(ride.price)
        ride.extra_tax = data.get('extra_tax')
        calc_tax = TaxRide()
        ride.tax_result = calc_tax.tax_used(ride.price, ride.extra_tax)
        ride.comment = data.get('comment')
        ride.save()
        messages.success(request, 'Поездка изменена!')
        return render(request, 'ride_done.html', {'ride': ride})
    return render(request, 'change_ride.html', {'form': form, 'ride': ride})


def delete_ride(request, number):
    ride = Ride.objects.get(number=number)
    ride.delete()
    rides = Ride.objects.all().order_by('shift', 'car')
    rides = prettify(rides)
    return render(request, 'ride_list.html', {'rides': rides})


def show_rides(request):
    rides = Ride.objects.all().order_by('shift', 'car') # to make filter by shift
    rides = prettify(rides)
    return render(request, 'ride_list.html', {'rides': rides})


def show_detail(request, number):
    ride = Ride.objects.get(number=number)
    return render(request, 'ride_detail.html', {'ride': ride})


def show_reports(request):
    reports = BalanceDriver.objects.all().order_by('day')
    return render(request, 'new_report_list.html', {'reports': reports})



class DriverDay(View):
    def get(self, request, name, shift):
        day = Shift.objects.get(date=shift)
        week = day.week
        week = week.week
        qs = Ride.objects.filter(shift__date=shift)
        rides = qs.filter(driver__name=name).order_by('number')
        rides = prettify(rides)
        form = TotalDayDriverForm(request.POST, week=week)
        try:
            report = BalanceDriver.objects.filter(day__date=shift).get(driver__name=name)
        except BalanceDriver.DoesNotExist:
            report = None
        return render(request, 'total/totalday_driver.html', {'rides': rides, 'name': name, 'shift': shift, 'week': week, 'form': form, 'report': report })

    def post(self, request, name, shift):
        day = Shift.objects.get(date=shift)
        week_d = day.week
        week = week_d.week
        form = TotalDayDriverForm(request.POST, week=week)
        if form.is_valid():
            data = form.cleaned_data
            shift = data['shift']
            shift = str(shift)
            gross = GrossDay()
            rides = gross.total_day_driver(shift, name)
            rides = prettify(rides)
            try:
                report = BalanceDriver.objects.filter(day__date=shift).get(driver__name=name)
            except BalanceDriver.DoesNotExist:
                report = None
            return render(request, 'total/totalday_driver.html', {'rides': rides, 'name': name, 'shift': shift, 'week': week, 'form': form, 'report': report })



class CarDay(View):
    def get(self, request, car, shift):
        day = Shift.objects.get(date=shift)
        week = day.week
        week = week.week
        qs = Ride.objects.filter(shift__date=shift)
        rides = qs.filter(car__plate=car).order_by('number')
        car_rides = prettify(rides)
        form = TotalDayCarForm(request.POST, week=week)
        return render(request, 'total/totalday_car.html', {'rides': car_rides, 'car': car, 'shift': shift, 'week': week, 'form': form })

    def post(self, request, car, shift):
        day = Shift.objects.get(date=shift)
        week_d = day.week
        week = week_d.week
        form = TotalDayCarForm(request.POST, week=week)
        if form.is_valid():
            data = form.cleaned_data
            shift = data['shift']
            shift = str(shift)
            gross = GrossDay()
            rides = gross.total_day_car(shift, car)
            rides = prettify(rides)
            return render(request, 'total/totalday_car.html', {'rides': rides, 'car': car, 'shift': shift, 'week': week, 'form': form })



class DriverWeek(View):
    def get(self, request, name, week):
        qs = Ride.objects.filter(driver__name=name).select_related('shift__week')
        weeks = []
        for i in qs:
            myweek = i.shift.week.week
            if myweek in weeks:
                pass
            else:
                weeks.append(myweek)
        weeks.sort()
        rides = qs.filter(shift__week__week=week).order_by('number')
        rides = prettify(rides)
        return render(request, 'total/totalweek_driver.html',
                      {'rides': rides, 'name': name, 'week': week, 'weeks': weeks})



class CarWeek(View):
    def get(self, request, car, week):
        qs = Ride.objects.filter(car__plate=car).select_related('shift__week')
        weeks = []
        for i in qs:
            myweek = i.shift.week.week
            if myweek in weeks:
                pass
            else:
                weeks.append(myweek)
        weeks.sort()
        rides = qs.filter(shift__week__week=week).order_by('number')
        rides = prettify(rides)
        return render(request, 'total/totalweek_car.html',
                      {'rides': rides, 'car': car, 'week': week, 'weeks': weeks})


def add_report(request, shift):
    balance_d = BalanceDriver()
    form = ReportDriverForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        balance_d.day = data.get('day')
        balance_d.driver = data.get('driver')
        balance_d.car = data.get('car')
        balance_d.miles_s = data.get('miles_s')
        balance_d.miles_f = data.get('miles_f')
        balance_d.mileage = balance_d.miles_f - balance_d.miles_s
        balance_d.hours = data.get('hours')
        balance_d.priority = data.get('priority')
        balance_d.wash = data.get('wash')
        balance_d.water = data.get('water')
        balance_d.other = data.get('other')
        mybalance = DriverDayBalance()
        mybalance.rides_result(balance_d.driver, shift)
        balance_d.tolls = mybalance.tolls
        balance_d.income = mybalance.income
        balance_d.cash = mybalance.cash
        balance_d.tips = mybalance.tips
        balance_d.s_tax = mybalance.s_tax
        balance_d.x_tax = mybalance.x_tax
        balance_d.save()
        return render(request, 'report_done.html', {'balance_d': balance_d})
    return render(request, 'add_report.html', {'form': form})