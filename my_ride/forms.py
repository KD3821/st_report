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
        fields = ['shift']

    # def __init__(self, request, *args, **kwargs):
    #     self.week = kwargs.pop('week', None)
    #     super().__init__(**kwargs)
    #     self.fields['shift'].queryset = Shift.objects.filter(week__week=self.week)

        # super().__init__(**kwargs)
        # if week:
        #     self.fields['shift'].queryset = Shift.objects.filter(week__week=week)

    def __init__(self, request, week, *args, **kwargs):
        super(TotalDayDriverForm, self).__init__(*args, **kwargs)
        self.fields['shift'].queryset = Shift.objects.filter(week__week=week)