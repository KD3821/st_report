from my_ride.models import Ride, ExtraTax



class GrossDay:
    def rides_day(self, shift):
        qs = Ride.objects.filter(shift__date=shift)
        return qs

    def total_day_car(self, shift, car):
        get_rides = self.rides_day(shift)
        qs = get_rides.filter(car__plate=car).order_by('number')
        return qs

    def total_day_driver(self, shift, name):
        get_rides = self.rides_day(shift)
        qs = get_rides.filter(driver__name=name).order_by('number')
        return qs



class SaveTax:
    def tax_saved(self, price):
        tax = round((price * 25.7 / 100), 2)
        return tax


class TaxRide:
    def tax_used(self, price, mode):
        used_tax = ExtraTax.objects.get(mode=mode)
        commission = round((price * used_tax.tax / 100), 2)
        return commission


