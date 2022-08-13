from django.shortcuts import render
from django.views import View
from .forms import RideForm, TotalCarForm
from .models import Ride
from django.contrib import messages
from total import GrossCar


def enter_ride(request):
    ride = Ride()
    form = RideForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        ride.number = data.get('number')
        ride.car = data.get('car')
        ride.driver = data.get('driver')
        ride.shift = data.get('shift')
        ride.price = data.get('price')
        ride.cash = data.get('cash')
        ride.toll = data.get('toll')
        ride.save_tax = data.get('save_tax')
        ride.extra_tax = data.get('extra_tax')
        ride.comment = data.get('comment')
        ride.save()
        messages.success(request, 'Поездка добавлена!')
        return render(request, 'ride_done.html', {'ride': ride})
    return render(request, 'add_ride.html', {'form': form})


def show_rides(request):
    rides = Ride.objects.all()
    for ride in rides:
        if ride.cash == False:
            ride.cash = '---'
        else:
            ride.cash = ride.price
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
        'cash': ride.cash,
        'toll': ride.toll,
        'save_tax': ride.save_tax,
        'extra_tax': ride.extra_tax,
        'comment': ride.comment
    })
    if form.is_valid():
        data = form.cleaned_data
        ride.number = data.get('number')
        ride.car = data.get('car')
        ride.driver = data.get('driver')
        ride.shift = data.get('shift')
        ride.price = data.get('price')
        ride.cash = data.get('cash')
        ride.toll = data.get('toll')
        ride.save_tax = data.get('save_tax')
        ride.extra_tax = data.get('extra_tax')
        ride.comment = data.get('comment')
        ride.save()
        messages.success(request, 'Поездка изменена!')
        return render(request, 'ride_detail.html', {'ride': ride})
    return render(request, 'ride_change.html', {'form': form, 'ride': ride})


class CarShift(View):
    def get(self, request):
        form = TotalCarForm()
        return render(request, 'total/totalcar.html', {'form': form})

    def post(self, request):
        form = TotalCarForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            shift, car = data['shift'], data['car']
            shift = str(shift)
            gross = GrossCar()
            # raw_result = gross.rides_day(shift)
            result = gross.rides_day_car(shift, car)
            return render(request, 'total/totalcar.html', {'result': result, 'form': form})