from django.db import models
from datetime import datetime, timedelta
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

# class Photo(models.Model):
#     uploader = models.CharField(max_length=255, blank=True, null=True)
#     imagen = models.ImageField(default='photos/photo.jpg', upload_to='photos')
#     titulo = models.CharField(max_length=50, blank=True, null=True)
#     descripcion = models.CharField(max_length=255, blank=True, null=True)
#     created_date = models.DateField(auto_now_add=True)



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

def get_expiration():
    return datetime.today() + timedelta(days=30)

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True,null=True
    )
    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=80)
    TYPE_CHOICES = [
        ("N", 'NUEVO'),
        ("U", 'USADO'),
        
    ]
    condicion = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES,
        default="USADO",
    )
    marca = models.CharField(max_length=40, blank=True)
    modelo = models.CharField(max_length=40, blank=True)
    year = models.IntegerField(null=True, blank=True, default=1990)
    numero_serie = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    entrega = models.CharField(max_length=255, blank=True, null=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    nombre = models.CharField(max_length=40)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    fecha_creada = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField(blank=True, default=get_expiration)
    active = models.BooleanField(default=True)
    images = models.CharField(max_length=2000, blank=True,null=True)
    def imageList(self):
        if self.images == None:
            return " "
        return self.images.split(';')

    def __str__(self):
        return self.titulo


# class ImageProduct(models.Model):
#     name = models.CharField(max_length=255)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(default='photos/photo.jpg', upload_to='products')
#     default = models.BooleanField(default=False)
#     order = models.SmallIntegerField(default=1)
