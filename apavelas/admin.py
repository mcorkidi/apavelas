from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Benefit)
admin.site.register(Event)
admin.site.register(Place)
admin.site.register(Photo)

admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Transaction)

