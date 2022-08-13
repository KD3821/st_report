from django.db import models
from django.db.models import DateField, DateTimeField, CharField, IntegerField, BooleanField, ForeignKey, TextField


class Shift(models.Model):
    date = DateField()

    def __str__(self):
        return f'{self.date}'


class Car(models.Model):
    plate = CharField(max_length=200)
    date = ForeignKey(Shift, on_delete=models.CASCADE)
    income = IntegerField(default=0)
    rides = IntegerField(default=0)
    fuel = IntegerField(default=0)
    wash = IntegerField(default=0)
    fix = IntegerField(default=0)
    service = IntegerField(default=0)
    other = IntegerField(default=0)

    def __str__(self):
        return self.plate


class Driver(models.Model):
    name = CharField(max_length=200)
    salary = IntegerField(default=0)
    tips = IntegerField(default=0)
    costs = IntegerField(default=0)
    owns = IntegerField(default=0)
    fines = IntegerField(default=0)

    def __str__(self):
        return self.name


class Ride(models.Model):
    number = CharField(max_length=100)
    driver = ForeignKey(Driver, on_delete=models.CASCADE)
    car = ForeignKey(Car, on_delete=models.CASCADE)
    shift = ForeignKey(Shift, on_delete=models.CASCADE)
    price = IntegerField(default=0)
    tip = IntegerField(default=0)
    cash = BooleanField(default=False)
    toll = IntegerField(default=0)
    save_tax = BooleanField(default=False)
    extra_tax = IntegerField(default=0)
    comment = TextField(max_length=200, blank=True)

    def __str__(self):
        return self.number

