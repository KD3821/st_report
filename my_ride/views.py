from django.shortcuts import render
from django.views import View
from .forms import RideForm, TotalDayDriverForm, TotalDayCarForm, TotalWeekDriverForm
from .models import Ride, Week, Shift
from django.contrib import messages
from total import GrossDay, GrossWeek, SaveTax, TaxRide


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



def show_rides(request):
    rides = Ride.objects.all().order_by('shift', 'car') # to make filter by shift
    rides = prettify(rides)
    return render(request, 'ride_list.html', {'rides': rides})



def show_detail(request, number):
    ride = Ride.objects.get(number=number)
    return render(request, 'ride_detail.html', {'ride': ride})



class DriverDay(View):
    def get(self, request, name, shift):
        day = Shift.objects.get(date=shift)
        week = day.week
        week = week.week
        qs = Ride.objects.filter(shift__date=shift)
        rides = qs.filter(driver__name=name).order_by('number')
        rides = prettify(rides)
        form = TotalDayDriverForm(request.POST, week=week)
        return render(request, 'total/totalday_driver.html', {'rides': rides, 'name': name, 'shift': shift, 'week': week, 'form': form })

    def post(self, request, name, shift):
        day = Shift.objects.get(date=shift)
        week_d = day.week
        week = week_d.week
        form = TotalDayDriverForm(request.POST, week=week)
        if form.is_valid():
            print('good')
            data = form.cleaned_data
            shift = data['shift']
            shift = str(shift)
            gross = GrossDay()
            rides = gross.total_day_driver(shift, name)
            rides = prettify(rides)
            return render(request, 'total/totalday_driver.html', {'rides': rides, 'name': name, 'shift': shift, 'week': week, 'form': form })



class CarDay(View):
    def get(self, request, car, shift):
        # shift = str(shift)
        # car = str(car)
        print(shift, car)
        day = Shift.objects.get(date=shift)
        print(day)
        week = day.week
        week = week.week
        qs = Ride.objects.filter(shift__date=shift)
        print(qs)
        rides = qs.filter(car__plate=car).order_by('number')
        print(rides)
        car_rides = prettify(rides)
        form = TotalDayCarForm(request.POST, week=week)
        return render(request, 'total/totalday_car.html', {'rides': car_rides, 'car': car, 'shift': shift, 'week': week, 'form': form })

    def post(self, request, car, shift):
        day = Shift.objects.get(date=shift)
        week_d = day.week
        week = week_d.week
        form = TotalDayCarForm(request.POST, week=week)
        if form.is_valid():
            print('good')
            data = form.cleaned_data
            shift = data['shift']
            shift = str(shift)
            gross = GrossDay()
            rides = gross.total_day_car(shift, car)
            rides = prettify(rides)
            return render(request, 'total/totalday_car.html', {'rides': rides, 'car': car, 'shift': shift, 'week': week, 'form': form })



class DriverWeek(View):
    def get(self, request, name, week):
        # day = Shift.objects.get(date=shift)
        # week = day.week
        # week = week.week
        qs = Ride.objects.filter(shift__week__week=week).filter(driver__name=name)
        rides = qs.order_by('number')
        rides = prettify(rides)
        return render(request, 'total/totalweek_driver.html',
                      {'rides': rides, 'name': name, 'week': week})


    # def get(self, request, name, shift):
    #     form = TotalDriverForm(initial={'name': name})
    #     return render(request, 'total/totalweek_driver.html', {'form': form})
    #
    # def post(self, request, name):
    #     form = TotalDriverForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         name = data['name']
    #         gross = GrossWeek()
    #         result = gross.rides_week_driver(name)
    #         return render(request, 'total/total_driver.html', {'result': result, 'form': form, 'name': name})


###########################


class CarWeek(View):
    pass
#     def get(self, request, car, shift):
#         pass
