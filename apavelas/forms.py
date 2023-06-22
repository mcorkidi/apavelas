from email.mime import image
from django import forms
from .models import *


class BenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = '__all__'


class PlacesForm(forms.ModelForm):
    CHOICES = [('ESCUELAS', 'ESCUELAS'), ('TIENDAS', 'TIENDAS'), 
    ('SPOTS', 'SPOTS'), ('HOTELES', 'HOTELES'), 
    ('RESTAURANTES', 'RESTAURANTES'), ('MEDICOS', 'MEDICOS')]
    class Meta:
        model=Place
        fields= '__all__'
        
    
    tipo_de_sitio = forms.ChoiceField(choices=CHOICES)

class EventsForm(forms.ModelForm):
    class Meta:
        model=Event
        fields = '__all__'



class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields='__all__'

class NewListingForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['titulo', 'condicion', 'marca', 'modelo', 'numero_serie', 'descripcion', 'precio', 'entrega', 'costo_envio',
                'nombre', 'telefono', 'correo']

       

