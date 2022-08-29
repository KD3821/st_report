from django.forms import ModelForm, Form, Textarea
from .models import Ride, Driver, Shift, Week


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


class TotalWeekDriverForm(ModelForm):
    class Meta:
        model = Week
        fields = ('week',)

    # def __init__(self, *args, **kwargs):
    #     driver = kwargs.pop('driver', None)
    #     super(TotalWeekDriverForm, self).__init__(*args, **kwargs)
    #     if driver:
    #         qs = Ride.objects.filter(driver__name=driver).select_related('shift__week')
    #
    #
    #         self.fields['week'].queryset = Week.objects.filter(week=week)