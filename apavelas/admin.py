from django.contrib import admin
from .models import *

admin.site.site_header = "Apavelas Administrator"
admin.site.site_title = "Apavelas Administrator"
admin.site.index_title = "Apavelas Administrator"

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'descripcion', 'amount', 'account', 'user']
    list_editable = ['user']
# Register your models here.

admin.site.register(Benefit)
admin.site.register(Event)
admin.site.register(Place)
admin.site.register(Photo)

admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(EmailList)

