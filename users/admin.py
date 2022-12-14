from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'active', 'validTo')
    list_editable = ['validTo']

# Register your models here.

admin.site.register(Profile, ProfileAdmin)