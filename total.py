from my_ride.models import Shift, Car, Driver, Ride



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