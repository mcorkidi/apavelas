from django import forms
from .models import *

class ProfileImageForm(forms.Form):
	
	foto_perfil = forms.ImageField()

class FaceImageForm(forms.Form):
	
	foto_tarjeta = forms.ImageField()



