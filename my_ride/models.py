from django.db import models
from django.db.models import DateField, DateTimeField, CharField, IntegerField, BooleanField, ForeignKey, TextField


class Week(models.Model):
    week = IntegerField(default=1)

    def __str__(self):
        return f'{self.week}'



class Shift(models.Model):
    date = DateField()
    week = ForeignKey(Week, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date}'




class Car(models.Model):
    plate = CharField(max_length=200)
    rental_rate = IntegerField(default=3000)

    def __str__(self):
        return self.plate



class Driver(models.Model):
    name = CharField(max_length=200)
    salary = IntegerField(default=0)
    tips = IntegerField(default=0)
    costs = IntegerField(default=0)
    deposit = IntegerField(default=0)
    fines = IntegerField(default=0)

    def __str__(self):
        return self.name



class ExtraTax(models.Model):
    mode = CharField(max_length=100)
    tax = IntegerField(default=0)

    def __str__(self):
        return self.mode



class Ride(models.Model):
    number = CharField(max_length=50)
    driver = ForeignKey(Driver, on_delete=models.CASCADE)
    car = ForeignKey(Car, on_delete=models.CASCADE)
    shift = ForeignKey(Shift, on_delete=models.CASCADE)
    price = IntegerField(default=0)
    tip = IntegerField(default=0)
    cash = BooleanField(default=False)
    toll = IntegerField(default=0)
    save_tax = BooleanField(default=False)
    saved_tax_result = IntegerField(default=0)
    extra_tax = ForeignKey(ExtraTax, on_delete=models.CASCADE)
    tax_result = IntegerField(default=0)
    comment = TextField(max_length=200, blank=True)

    def __str__(self):
        return self.number



class Balance(models.Model):
    day = ForeignKey(Shift, on_delete=models.CASCADE)
    car = ForeignKey(Car, on_delete=models.CASCADE)
    driver = ForeignKey(Driver, on_delete=models.CASCADE)
    fuel = IntegerField(default=0)
    wash = IntegerField(default=0)
    service = IntegerField(default=0)
    repair = IntegerField(default=0)
    other = IntegerField(default=0)
    income = IntegerField(default=0)
    s_tax = IntegerField(default=0)
    x_tax = IntegerField(default=0)
    salary = IntegerField(default=0)
    note = CharField(max_length=200)

    def __str__(self):
        return f'{self.day} - {self.car}'



class BalanceDriver(models.Model):
    day = ForeignKey(Shift, on_delete=models.CASCADE)
    driver = ForeignKey(Driver, on_delete=models.CASCADE)
    car = ForeignKey(Car, on_delete=models.CASCADE)
    miles_s = IntegerField(default=0)
    miles_f = IntegerField(default=0)
    buy_s = IntegerField(default=0)
    hours = IntegerField(default=0)
    priority = IntegerField(default=0)
    wash = IntegerField(default=0)
    water = IntegerField(default=0)
    fuel = IntegerField(default=0)
    other = IntegerField(default=0)
    tolls = IntegerField(default=0)
    income = IntegerField(default=0)
    cash = IntegerField(default=0)
    tips = IntegerField(default=0)
    s_tax = IntegerField(default=0)
    x_tax = IntegerField(default=0)
    comment = CharField(max_length=300, blank=True)
    mileage = IntegerField(default=0)

    def __str__(self):
        return f'{self.day} - {self.driver}'



class BalanceCar(models.Model):
    c_day = ForeignKey(Shift, on_delete=models.CASCADE)
    c_car = ForeignKey(Car, on_delete=models.CASCADE)
    c_driver = ForeignKey(Driver, on_delete=models.CASCADE)
    c_info = ForeignKey(BalanceDriver, on_delete=models.CASCADE)
    c_fuel = IntegerField(default=0)
    c_wash = IntegerField(default=0)
    c_toll = IntegerField(default=0)
    c_fine = IntegerField(default=0)
    c_service = IntegerField(default=0)
    c_repair = IntegerField(default=0)

    def __str__(self):
        return f'{self.c_car} - {self.c_day}'