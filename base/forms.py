from django.forms import ModelForm
from django import forms
from .models import Ticket, Bus

def getChoices():
    buses = Bus.objects.all()
    bus_dict = {}
    for bus in buses:
        try:
            count_ticket = Ticket.objects.get(vehicle=bus).count()
        except:
            count_ticket = 0
        if count_ticket < bus.capacity:
            bus_dict[bus.id] = bus.name

    bus_arr = list(bus_dict.items())
    choices = tuple(bus_arr)

    return choices  
      

class TicketForm(forms.Form):
    first_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))
    vehicle = forms.ChoiceField(choices=getChoices, required=True, widget=forms.Select(attrs={'class':'form-control'}))

class VehicleForm(ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'
        widgets = {
                    'capacity' : forms.NumberInput(attrs={'class':'form-control'}),
                    'name': forms.TextInput(attrs={'class':'form-control'}),
                    'model_name': forms.TextInput(attrs={'class':'form-control'}),
                    'number': forms.TextInput(attrs={'class':'form-control', 'max': '12'})          
            }  
