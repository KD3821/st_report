from django.db.models import IntegerField
from my_ride.models import Ride, Car, Shift, Driver, BalanceDriver


class DriverDayBalance:
    income = IntegerField(default=0)
    tolls = IntegerField(default=0)
    cash = IntegerField(default=0)
    tips = IntegerField(default=0)
    s_tax = IntegerField(default=0)
    x_tax = IntegerField(default=0)
    # mileage = IntegerField(default=0)

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