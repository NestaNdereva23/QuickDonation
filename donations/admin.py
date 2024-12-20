from django.contrib import admin
from .models import Organizations, Donation, Transaction
# Register your models here.

admin.site.register(Organizations)
admin.site.register(Donation)
admin.site.register(Transaction)