from my_ride.models import Shift, Car, Driver, Ride, ExtraTax



class GrossCar:
    def rides_day(self, shift):
        qs1 = Ride.objects.filter(shift__date=shift)
        return qs1

    def rides_day_car(self, shift, car):
        get_rides = self.rides_day(shift)
        qs2 = get_rides.filter(car__plate=car)
        return qs2


class GrossDriver:
    def rides_week(self, name):
        qs = Ride.objects.filter(driver__name=name)
        return qs

class SaveTax:
    def tax_saved(self, number):
        notax_ride = Ride.objects.get(number=number)
        tax = round((notax_ride.price * 25.7 / 100), 2)
        return tax


class TaxRide:
    def tax_used(self, number, mode):
        taxed_ride = Ride.objects.get(number=number)
        used_tax = ExtraTax.objects.get(mode=mode)
        commission = round((taxed_ride.price * used_tax.tax / 100), 2)
        return commission