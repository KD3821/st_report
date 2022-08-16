from django.shortcuts import render
from django.views import View
from .forms import RideForm, TotalCarForm, TotalDriverForm
from .models import Ride, ExtraTax
from django.contrib import messages
from total import GrossDay, GrossWeek, SaveTax, TaxRide


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
            ride.saved_tax_result = tax.tax_saved(ride.number)
        ride.extra_tax = data.get('extra_tax')
        calc_tax = TaxRide()
        ride.tax_result = calc_tax.tax_used(ride.number, ride.extra_tax)
        ride.comment = data.get('comment')
        ride.save()
        messages.success(request, 'Поездка добавлена!')
        return render(request, 'ride_done.html', {'ride': ride})
    return render(request, 'add_ride.html', {'form': form})


def show_rides(request):
    rides = Ride.objects.all() # to make filter by shift
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
            ride.tax_result = '---'
        if ride.toll == 0:
            ride.toll = '---'
        if ride.tip == 0:
            ride.tip = '---'
    return render(request, 'ride_list.html', {'rides': rides})


def show_detail(request, number):
    ride = Ride.objects.get(number=number)
    return render(request, 'ride_detail.html', {'ride': ride})


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
            ride.saved_tax_result = tax.tax_saved(ride.number)
        ride.extra_tax = data.get('extra_tax')
        calc_tax = TaxRide()
        ride.tax_result = calc_tax.tax_used(ride.number, ride.extra_tax)
        ride.comment = data.get('comment')
        ride.save()
        messages.success(request, 'Поездка изменена!')
        return render(request, 'ride_detail.html', {'ride': ride})
    return render(request, 'ride_change.html', {'form': form, 'ride': ride})


class CarShift(View):
    def get(self, request, car):
        form = TotalCarForm(initial={'car': car})
        return render(request, 'total/totalcar.html', {'form': form})

    def post(self, request, car):
        form = TotalCarForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            shift, car = data['shift'], data['car']
            shift = str(shift)
            gross = GrossDay()
            result = gross.rides_day_car(shift, car)
            return render(request, 'total/totalcar.html', {'result': result, 'form': form})

class DriverWeek(View):
    def get(self, request, name):
        form = TotalDriverForm(initial={'name': name})
        return render(request, 'total/totaldriver.html', {'form': form})

    def post(self, request, name):
        form = TotalDriverForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            gross = GrossWeek()
            result = gross.rides_week_driver(name)
            return render(request, 'total/totaldriver.html', {'result': result, 'form': form})