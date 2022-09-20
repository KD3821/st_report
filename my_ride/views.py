from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from .forms import RideForm, TotalDayDriverForm, TotalDayCarForm, ReportDriverForm, SelectDriverForm, AddPlanForm, SelectWeekForm
from .models import Ride, Week, Shift, BalanceDriver, Driver, PlanShift
from django.contrib import messages
from total import GrossDay, SaveTax, TaxRide
from accounting import DriverDayBalance, DriverWeekBalance
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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



def edit_ride(request, number, name):
    ride = Ride.objects.filter(driver__name=name).get(number=number)
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


def show_detail(request, number, name):
    ride = Ride.objects.filter(driver__name=name).get(number=number)
    return render(request, 'ride_detail.html', {'ride': ride})


def show_week_reports(request, week):
    days = Shift.objects.filter(week__week=week)
    form = SelectDriverForm(request.POST)
    weekly_reports = {}
    weekly_plans = {}
    for i in days:
        week_reports = BalanceDriver.objects.filter(day=i).order_by('car')
        weekly_reports[i] = week_reports
        week_plans = PlanShift.objects.filter(plan_day=i).order_by('plan_car')
        weekly_plans[i] = week_plans
    if form.is_valid():
        data = form.cleaned_data
        driver = data['driver']
        for i in days:
            week_reports = BalanceDriver.objects.filter(day=i).filter(driver__name=driver).order_by('car')
            weekly_reports[i] = week_reports
            week_plans = PlanShift.objects.filter(plan_day=i).filter(plan_driver__name=driver).order_by('plan_car')
            weekly_plans[i] = week_plans
        week_calc = DriverWeekBalance()
        week_calc.week_result(driver, week)
        salary = week_calc.salary
        tips = week_calc.tips
        buy = week_calc.buy
        saved_tax = week_calc.saved_tax
        extra_tax = week_calc.extra_tax
        cash = week_calc.cash
        tolls = week_calc.tolls
        wash = week_calc.wash
        water = week_calc.water
        other = week_calc.other
        hours = week_calc.hours
        mileage = week_calc.mileage
        return render(request, 'week_page.html', {
            'week': week,
            'weekly_reports': weekly_reports.items(),
            'weekly_plans': weekly_plans.items(),
            'form': form,
            'driver': driver,
            'salary': salary,
            'tips': tips,
            'buy': buy,
            'saved_tax': saved_tax,
            'extra_tax': extra_tax,
            'cash': cash,
            'tolls': tolls,
            'wash': wash,
            'water': water,
            'other': other,
            'hours': hours,
            'mileage': mileage
        })
    return render(request, 'week_page.html', {'week': week, 'weekly_reports': weekly_reports.items(), 'weekly_plans': weekly_plans.items(), 'form': form})


def show_weeks(request):
    weeks = Week.objects.all().order_by('week')
    return render(request, 'start_page.html', {
        'weeks': weeks
    })



class DriverDay(View):
    def get(self, request, name, shift):
        day = Shift.objects.get(date=shift)
        week = day.week
        week = week.week
        qs = Ride.objects.filter(shift__date=shift)
        rides = qs.filter(driver__name=name).order_by('number')
        # plan = PlanShift.objects.filter(plan_day__date=shift).filter(plan_driver__name=name)[0:1].get()
        if rides:
            get_car = rides[0]
            car = get_car.car
        # elif plan:
        #     car = plan.plan_car
        else:
            try:
                plan = PlanShift.objects.filter(plan_day__date=shift).filter(plan_driver__name=name)[0:1].get()
                car = plan.plan_car
            except PlanShift.DoesNotExist:
                car = '-----'
        rides = prettify(rides)
        d_form = TotalDayDriverForm(request.POST, week=week)
        c_form = TotalDayCarForm(request.POST, week=week)
        try:
            report = BalanceDriver.objects.filter(day__date=shift).get(driver__name=name)
        except BalanceDriver.DoesNotExist:
            report = None
        return render(request, 'total/totalday_driver.html', {'rides': rides, 'name': name, 'shift': shift, 'week': week, 'd_form': d_form, 'c_form': c_form, 'car': car, 'report': report })

    def post(self, request, name, shift):
        day = Shift.objects.get(date=shift)
        week_d = day.week
        week = week_d.week
        qs = Ride.objects.filter(shift__date=shift).filter(driver__name=name)
        if qs:
            get_car = qs[0]
            car = get_car.car
        else:
            car = '-----'
        d_form = TotalDayDriverForm(request.POST, week=week)
        c_form = TotalDayCarForm(request.POST, week=week)
        if 'driver_sub' in request.POST:
            if d_form.is_valid():
                data = d_form.cleaned_data
                shift = data['shift']
                shift = str(shift)
                return HttpResponseRedirect(reverse('total_day_driver', args=[name, shift]))
        elif 'car_sub' in request.POST:
            if c_form.is_valid():
                data = c_form.cleaned_data
                shift = data['shift']
                shift = str(shift)
                gross = GrossDay()
                rides = gross.total_day_car(shift, car)
                if rides:
                    get_name = rides[0]
                    name = get_name.driver
                else:
                    name = '-----'
                return HttpResponseRedirect(reverse('total_day_driver', args=[name, shift]))



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


def add_report(request, shift, name):
    balance_d = BalanceDriver()
    day = Shift.objects.get(date=shift)
    week = day.week
    try:
        driver = Driver.objects.get(name=name)
    except Driver.DoesNotExist:
        return render(request, '404.html', {'week': week})
    try:
        ride = Ride.objects.filter(shift=day).filter(driver__name=name)[0:1].get()
    except Ride.DoesNotExist:
        return render(request, '404.html', {'week': week})
    car = ride.car
    form = ReportDriverForm(request.POST or None, initial={
        'day': day,
        'driver': driver,
        'car': car
    })
    if form.is_valid():
        data = form.cleaned_data
        balance_d.day = data.get('day')
        balance_d.driver = data.get('driver')
        balance_d.car = data.get('car')
        balance_d.miles_s = data.get('miles_s')
        balance_d.miles_f = data.get('miles_f')
        balance_d.mileage = balance_d.miles_f - balance_d.miles_s
        balance_d.buy_s = data.get('buy_s')
        balance_d.hours = data.get('hours')
        balance_d.priority = data.get('priority')
        balance_d.fuel = data.get('fuel')
        balance_d.wash = data.get('wash')
        balance_d.water = data.get('water')
        balance_d.other = data.get('other')
        balance_d.comment = data.get('comment')
        mybalance = DriverDayBalance()
        mybalance.rides_result(balance_d.driver, shift)
        balance_d.tolls = mybalance.tolls
        balance_d.income = mybalance.income
        balance_d.cash = mybalance.cash
        balance_d.tips = mybalance.tips
        balance_d.s_tax = mybalance.s_tax
        balance_d.x_tax = mybalance.x_tax
        balance_d.save()
        return render(request, 'report_done.html', {'balance_d': balance_d, 'week': week})
    return render(request, 'add_report.html', {'form': form, 'week': week})


def edit_report(request, shift, name):
    day = Shift.objects.get(date=shift)
    week = day.week
    try:
        report = BalanceDriver.objects.filter(day__date=shift).get(driver__name=name)
    except BalanceDriver.DoesNotExist:
        return render(request, '404.html', {'week': week})
    form = ReportDriverForm(request.POST or None, initial={
        'day': report.day,
        'driver': report.driver,
        'car': report.car,
        'miles_s': report.miles_s,
        'miles_f': report.miles_f,
        'hours': report.hours,
        'buy_s': report.buy_s,
        'priority': report.priority,
        'fuel': report.fuel,
        'wash': report.wash,
        'water': report.water,
        'other': report.other,
        'comment': report.comment
    })
    if form.is_valid():
        data = form.cleaned_data
        report.day = data.get('day')
        report.driver = data.get('driver')
        report.car = data.get('car')
        report.miles_s = data.get('miles_s')
        report.miles_f = data.get('miles_f')
        report.mileage = report.miles_f - report.miles_s
        report.buy_s = data.get('buy_s')
        report.hours = data.get('hours')
        report.priority = data.get('priority')
        report.fuel = data.get('fuel')
        report.wash = data.get('wash')
        report.water = data.get('water')
        report.other = data.get('other')
        report.comment = data.get('comment')
        mybalance = DriverDayBalance()
        mybalance.rides_result(report.driver, shift)
        report.tolls = mybalance.tolls
        report.income = mybalance.income
        report.cash = mybalance.cash
        report.tips = mybalance.tips
        report.s_tax = mybalance.s_tax
        report.x_tax = mybalance.x_tax
        report.save()
        return render(request, 'report_done.html', {'balance_d': report, 'week': week})
    return render(request, 'add_report.html', {'form': form, 'week': week})


def add_plan(request, week):
    plan_shift = PlanShift()
    form = AddPlanForm(request.POST or None, week=week)
    if form.is_valid():
        data = form.cleaned_data
        plan_shift.plan_day = data.get('plan_day')
        plan_shift.plan_driver = data.get('plan_driver')
        plan_shift.plan_car = data.get('plan_car')
        try:
            c_busy = PlanShift.objects.filter(plan_day=plan_shift.plan_day).filter(plan_car=plan_shift.plan_car)[0:1].get()
            if c_busy:
                warning = 'Авто уже занято в этот день!'
                messages.error(request, 'А/м уже назначен для другого водителя.')
                return render(request, '404_plan.html', {'week': week, 'warning': warning})
        except PlanShift.DoesNotExist:
            try:
                d_busy = PlanShift.objects.filter(plan_day=plan_shift.plan_day).filter(plan_driver=plan_shift.plan_driver)[0:1].get()
                if d_busy:
                    warning = 'Водитель уже занят в этот день!'
                    messages.error(request, 'Водитель уже назначен на другой а/м.')
                    return render(request, '404_plan.html', {'week': week, 'warning': warning})
            except PlanShift.DoesNotExist:
                messages.success(request, 'Смена успешно запланирована.')
                plan_shift.save()
                return render(request, 'plan_done.html', {'plan_shift': plan_shift, 'week': week})
    return render(request, 'add_plan.html', {'form': form, 'week': week})


def x_plan(request, name, shift):
    plan = PlanShift.objects.filter(plan_day__date=shift).filter(plan_driver__name=name)[0:1].get()
    week = plan.plan_day.week
    plan.delete()
    return HttpResponseRedirect(reverse('plan_all', args=[week]))


def show_plan(request, week):
    form = SelectWeekForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        week = data.get('week')
        week = week.week
    days = Shift.objects.filter(week__week=week)
    weekly_plans = {}
    for day in days:
        week_plans = PlanShift.objects.filter(plan_day=day).order_by('plan_car')
        weekly_plans[day] = week_plans
    return render(request, 'plan_page.html', {'plans': weekly_plans.items(), 'week': week, 'form': form})


def edit_plan(request, week, name, shift):
    plan = PlanShift.objects.filter(plan_day__date=shift).filter(plan_driver__name=name)[0:1].get()
    plan_try = PlanShift.objects.filter(plan_day__date=shift).filter(plan_driver__name=name)[0:1].get()
    form = AddPlanForm(request.POST or None, initial={
        'plan_day': plan.plan_day,
        'plan_car': plan.plan_car,
        'plan_driver': plan.plan_driver
    })
    if form.is_valid():
        data = form.cleaned_data
        plan.plan_day = data.get('plan_day')
        plan.plan_driver = data.get('plan_driver')
        plan.plan_car = data.get('plan_car')
        plan.delete()
        try:
            c_busy = PlanShift.objects.filter(plan_day=plan.plan_day).filter(plan_car=plan.plan_car)[0:1].get()
            if c_busy:
                warning = 'Авто уже занято в этот день!'
                messages.error(request, 'А/м уже назначен для другого водителя.')
                plan_try.save()
                return render(request, '404_plan.html', {'week': week, 'warning': warning})
        except PlanShift.DoesNotExist:
            try:
                d_busy = PlanShift.objects.filter(plan_day=plan.plan_day).filter(plan_driver=plan.plan_driver)[0:1].get()
                if d_busy:
                    warning = 'Водитель уже занят в этот день!'
                    messages.error(request, 'Водитель уже назначен на другой а/м.')
                    plan_try.save()
                    return render(request, '404_plan.html', {'week': week, 'warning': warning})
            except PlanShift.DoesNotExist:
                messages.success(request, 'Данные по смене успешно изменены.')
                plan.save()
                return render(request, 'plan_done.html', {'plan_shift': plan, 'week': week})
    return render(request, 'add_plan.html', {'form': form, 'week': week})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('start')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

@login_required
def secret_page(request):
    return render(request, 'secret_page.html')