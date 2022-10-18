from django.forms import ModelForm, Textarea, ChoiceField
from .models import Driver, Car, Ride, Shift, BalanceDriver, PlanShift


class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['number', 'car', 'driver', 'shift', 'price', 'cash', 'toll', 'save_tax', 'extra_tax', 'tip', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 100, 'rows': 1}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        week = kwargs.pop('week', None)
        super(RideForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['car'].queryset = Car.objects.filter(user__username=user)
            self.fields['driver'].queryset = Driver.objects.filter(user__username=user)
        if week:
            self.fields['shift'].queryset = Shift.objects.filter(week__week=week)

class TotalDayDriverForm(ModelForm):
    class Meta:
        model = Ride
        fields = ('shift',)

    def __init__(self, *args, **kwargs):
        week = kwargs.pop('week', None)
        super(TotalDayDriverForm, self).__init__(*args, **kwargs)
        if week:
            self.fields['shift'].queryset = Shift.objects.filter(week__week=week)


class TotalDayCarForm(ModelForm):
    class Meta:
        model = Ride
        fields = ('shift',)

    def __init__(self, *args, **kwargs):
        week = kwargs.pop('week', None)
        super(TotalDayCarForm, self).__init__(*args, **kwargs)
        if week:
            self.fields['shift'].queryset = Shift.objects.filter(week__week=week)


class ReportDriverForm(ModelForm):
    buy_s = ChoiceField(choices=[(0, 'нет'), (1460, 'будний'), (1670, 'выходной')], label='Цена покупки смены')

    class Meta:
        model = BalanceDriver
        fields = ['day', 'driver', 'car', 'miles_s', 'miles_f', 'buy_s', 'hours', 'priority', 'fuel', 'wash', 'water', 'other', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 100, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        week = kwargs.pop('week', None)
        user = kwargs.pop('user', None)
        super(ReportDriverForm, self).__init__(*args, **kwargs)
        if week:
            self.fields['day'].queryset = Shift.objects.filter(week__week=week)
        if user:
            self.fields['car'].queryset = Car.objects.filter(user__username=user)
            self.fields['driver'].queryset = Driver.objects.filter(user__username=user)


class SelectDriverForm(ModelForm):
    class Meta:
        model = BalanceDriver
        fields = ('driver',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SelectDriverForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['driver'].queryset = Driver.objects.filter(user__username=user)


class AddPlanForm(ModelForm):
    class Meta:
        model = PlanShift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        week = kwargs.pop('week', None)
        user = kwargs.pop('user', None)
        super(AddPlanForm, self).__init__(*args, **kwargs)
        if week:
            self.fields['plan_day'].queryset = Shift.objects.filter(week__week=week)
        if user:
            self.fields['plan_car'].queryset = Car.objects.filter(user=user)
            self.fields['plan_driver'].queryset = Driver.objects.filter(user=user)


class SelectWeekForm(ModelForm):
    class Meta:
        model = Shift
        fields = ['week',]