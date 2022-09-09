from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Benefit(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(default='benefits/benefit.jpg', upload_to='benefits')
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    sitioweb = models.URLField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creada = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField(blank=True, default=datetime.now)



class Place(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(default='places/place.jpg', upload_to='places')
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    sitioweb = models.URLField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    tipo_de_sitio = models.CharField(max_length=255, blank=True, null=True)
 

class Event(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(default='events/event.jpg', upload_to='events')
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    sitioweb = models.URLField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    fecha_de_evento = models.DateField(blank=True, default=datetime.now)

class Photo(models.Model):
    uploader = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(default='photos/photo.jpg', upload_to='photos')
    titulo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)



