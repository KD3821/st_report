from django.db import models
from django.contrib.auth.models import User
from django.db.models import DateField, CharField, IntegerField, BooleanField, ForeignKey, TextField


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
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    plate = CharField(max_length=200)
    rental_rate = IntegerField(default=3000)

    def __str__(self):
        return self.plate



class Driver(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='drivers')
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
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    number = CharField(max_length=50, verbose_name='Номер заказа')
    driver = ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    car = ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Авто')
    shift = ForeignKey(Shift, on_delete=models.CASCADE, verbose_name='День')
    price = IntegerField(default=0, verbose_name='Стоимость')
    tip = IntegerField(default=0, verbose_name='Чаевые')
    cash = BooleanField(default=False, verbose_name='За наличные')
    toll = IntegerField(default=0, verbose_name='ЗСД')
    save_tax = BooleanField(default=False, verbose_name='С покупкой смены')
    saved_tax_result = IntegerField(default=0, verbose_name='Экономия комиссии')
    extra_tax = ForeignKey(ExtraTax, on_delete=models.CASCADE, verbose_name='Режим доп.комиссии')
    tax_result = IntegerField(default=0, verbose_name='Сумма доп.комиссии')
    comment = TextField(max_length=200, blank=True, verbose_name='Комментарий')

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
    day = ForeignKey(Shift, on_delete=models.CASCADE, verbose_name='День')
    driver = ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    car = ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Авто')
    miles_s = IntegerField(default=0, verbose_name='Пробег в начале смены')
    miles_f = IntegerField(default=0, verbose_name='Пробег в конце смены')
    buy_s = IntegerField(default=0, verbose_name='Цена покупки смены')
    hours = IntegerField(default=0, verbose_name='Часы на линии')
    priority = IntegerField(default=0, verbose_name='Приоритет +')
    wash = IntegerField(default=0, verbose_name='Мойка')
    water = IntegerField(default=0, verbose_name='Вода')
    fuel = IntegerField(default=0, verbose_name='Топливо')
    other = IntegerField(default=0, verbose_name='Прочее')
    tolls = IntegerField(default=0, verbose_name='ЗСД')
    income = IntegerField(default=0, verbose_name='Выручка')
    cash = IntegerField(default=0, verbose_name='Наличные')
    tips = IntegerField(default=0, verbose_name='Чаевые б/н')
    s_tax = IntegerField(default=0, verbose_name='Съэкономленная комиссия')
    x_tax = IntegerField(default=0, verbose_name='Сумма доп.комиссий')
    comment = CharField(max_length=300, blank=True, verbose_name='Комментарий')
    mileage = IntegerField(default=0, verbose_name='Пробег')

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


class PlanShift(models.Model):
    plan_day = ForeignKey(Shift, on_delete=models.CASCADE)
    plan_car = ForeignKey(Car, on_delete=models.CASCADE)
    plan_driver = ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.plan_day}-{self.plan_car}'