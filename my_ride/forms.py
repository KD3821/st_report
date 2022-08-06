from django.forms import ModelForm
from .models import Ride

class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['number', 'car', 'driver', 'shift', 'price', 'cash', 'toll', 'save_tax', 'extra_tax', 'comment']
