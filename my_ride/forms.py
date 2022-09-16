from django.forms import ModelForm, Textarea, ChoiceField
from .models import Ride, Shift, BalanceDriver, PlanShift


class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['number', 'car', 'driver', 'shift', 'price', 'cash', 'toll', 'save_tax', 'extra_tax', 'tip', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 100, 'rows': 1}),
        }


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
    buy_s = ChoiceField(choices=[(0, 'нет'), (1460, 'будний'), (1670, 'выходной')])

    class Meta:
        model = BalanceDriver
        fields = ['day', 'driver', 'car', 'miles_s', 'miles_f', 'buy_s', 'hours', 'priority', 'fuel', 'wash', 'water', 'other', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 100, 'rows': 1}),
        }


class SelectDriverForm(ModelForm):
    class Meta:
        model = BalanceDriver
        fields = ['driver',]


class AddPlanForm(ModelForm):
    class Meta:
        model = PlanShift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        week = kwargs.pop('week', None)
        super(AddPlanForm, self).__init__(*args, **kwargs)
        if week:
            self.fields['plan_day'].queryset = Shift.objects.filter(week__week=week)