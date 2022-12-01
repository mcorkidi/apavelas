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

    def __str__(self):
        return self.nombre



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

    def __str__(self):
        return self.nombre
 

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

    def __str__(self):
        return self.nombre

class Photo(models.Model):
    uploader = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(default='photos/photo.jpg', upload_to='photos')
    titulo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)



class Bank(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return self.name

class Account(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
   

    def __str__(self):
        return self.name


class Transaction(models.Model):
    fecha = models.DateTimeField(default=datetime.now)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    INCOME = 'INGRESO'
    EXPENSE = 'GASTO'
    
    TYPE_CHOICES = [
        (INCOME, 'INGRESO'),
        (EXPENSE, 'GASTO'),
        
    ]
    type_of_transaction = models.CharField(
        max_length=7,
        choices=TYPE_CHOICES,
        default=INCOME,
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.descripcion

class EmailList(models.Model):
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.email



