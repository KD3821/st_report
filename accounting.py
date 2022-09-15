from django.db.models import IntegerField
from my_ride.models import Ride, Car, Shift, Driver, BalanceDriver


class DriverDayBalance:
    income = IntegerField(default=0)
    tolls = IntegerField(default=0)
    cash = IntegerField(default=0)
    tips = IntegerField(default=0)
    s_tax = IntegerField(default=0)
    x_tax = IntegerField(default=0)
    mileage = IntegerField(default=0)

    def rides_result(self, name, shift):
        qs = Ride.objects.filter(driver=name).select_related('shift__week')
        self.income = 0
        self.tolls = 0
        self.cash = 0
        self.tips = 0
        self.s_tax = 0
        self.x_tax = 0
        qs1 = qs.filter(shift__date=shift)
        for i in qs1:
            self.income += i.price
            self.tolls += i.toll
            if i.cash == True:
                self.cash += i.price
            self.tips += i.tip
            if i.save_tax == True:
                self.s_tax += i.saved_tax_result
            self.x_tax += i.tax_result
        return {'income': self.income, 'tolls': self.tolls, 'cash': self.cash, 'tips': self.tips, 's_tax': self.s_tax, 'x_tax': self.x_tax}



class DriverWeekBalance:
    salary = IntegerField(default=0)
    tips = IntegerField(default=0)
    buy = IntegerField(default=0)
    saved_tax = IntegerField(default=0)
    extra_tax = IntegerField(default=0)
    cash = IntegerField(default=0)
    tolls = IntegerField(default=0)
    wash = IntegerField(default=0)
    water = IntegerField(default=0)
    other = IntegerField(default=0)

    def week_result(self, name, week):
        self.salary = 0
        self.tips = 0
        self.buy = 0
        self.saved_tax = 0
        self.extra_tax = 0
        self.cash = 0
        self.tolls = 0
        self.wash = 0
        self.water = 0
        self.other = 0
        self.hours = 0
        self.mileage = 0
        days = Shift.objects.filter(week__week=week)
        dayres_list = []
        for day in days:
            dayres = BalanceDriver.objects.filter(day=day).filter(driver=name)
            if dayres:
                dayres_list.append(dayres)
        for i in dayres_list:
            b = i[0]
            if b.income >= 1000:
                self.salary += (b.income / 100) * 35
            else:
                self.salary += (b.income / 100) * 30
            self.tips += b.tips
            self.buy += b.buy_s
            self.saved_tax += b.s_tax
            self.extra_tax += b.x_tax
            self.cash += b.cash
            self.tolls += b.tolls
            self.wash += b.wash
            self.water += b.water
            self.other += b.other
            self.hours += b.hours
            self.mileage += b.mileage
        return {
            'salary': self.salary,
            'tips': self.tips,
            'buy': self.buy,
            'saved_tax': self.saved_tax,
            'extra_tax': self.extra_tax,
            'cash': self.cash,
            'tolls': self.tolls,
            'wash': self.wash,
            'water': self.water,
            'other': self.other,
            'hours': self.hours,
            'mileage': self.mileage
        }