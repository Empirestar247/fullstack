from django.contrib import admin

# Register your models here.

from .models import Items, Shipment, Tracking

admin.site.register(Items)
admin.site.register(Shipment)
admin.site.register(Tracking)