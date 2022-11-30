from django.db import models
from django.contrib.auth.models import User
import uuid

from datetime import datetime
# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_pictures')
    faceImage = models.ImageField(default='facepic.jpg', upload_to='face_pictures')
    telephone = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    memberSince = models.DateField(blank=True, default=datetime.now)
    validTo = models.DateField(blank=True, default=datetime.now)
    qrcode = models.CharField(max_length=200, blank=True, default="")
    S = 'SMALL'
    Med = 'MEDIUM'
    L = 'LARGE'
    XL = 'EXTRA LARGE'
    SIZE_CHOICES = [
        (S, 'SMALL'),
        (Med,'MEDIUM'),
        (L, 'LARGE'),
        (XL, 'EXTRA LARGE')
    ]
    talla = models.CharField(
        max_length=12,
        choices=SIZE_CHOICES,
        default=Med,
    )
    P = 'PRESIDENTE'
    VP = 'VICEPRESIDENTE'
    S = 'SECRETARIO'
    T = 'TESORERO'
    D = 'DIRECTIVO'
    M = 'MIEMBRO'
    TYPE_CHOICES = [
        (P, 'PRESIDENTE'),
        (VP, 'VICEPRESIDENTE'),
        (S, 'SECRETARIO'),
        (T, 'TESORERO'),
        (D, 'DIRECTIVO'),
        (M, 'MIEMBRO'),

        
    ]
    type_of_member = models.CharField(
        max_length=14,
        choices=TYPE_CHOICES,
        default=M,
    )

    


    def __str__(self):
        return self.user.username

