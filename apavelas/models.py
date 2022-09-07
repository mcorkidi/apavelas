from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Benefit(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='benefit.jpg', upload_to='benefits')
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(blank=True, default=datetime.now)



class Place(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='place.jpg', upload_to='places')
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    type_of_place = models.CharField(max_length=255, blank=True, null=True)
 

class Event(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='event.jpg', upload_to='events')
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    date = models.DateField(blank=True, default=datetime.now)

class Photo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='photo.jpg', upload_to='photos')
    descrition = models.CharField(max_length=255, blank=True, null=True)



