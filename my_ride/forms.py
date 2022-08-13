from django.forms import ModelForm, Form, Textarea
from .models import Ride, Driver

class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['number', 'car', 'driver', 'shift', 'price', 'cash', 'toll', 'save_tax', 'extra_tax', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 100, 'rows': 1}),
        }


class TotalCarForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['shift', 'car']


class TotalDriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['name']