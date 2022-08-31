from django import forms

class ProfileImageForm(forms.Form):
	
	foto_perfil = forms.ImageField()

class FaceImageForm(forms.Form):
	
	foto_tarjeta = forms.ImageField()
