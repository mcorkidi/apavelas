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

class GalleryForm(forms.ModelForm):
    class Meta:
        model=Photo
        fields='__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["uploader"].disabled = True

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields='__all__'


       

