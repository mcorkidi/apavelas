from django.contrib import admin
from .models import Benefit, Event, Place, Photo

# Register your models here.

admin.site.register(Benefit)
admin.site.register(Event)
admin.site.register(Place)
admin.site.register(Photo)
