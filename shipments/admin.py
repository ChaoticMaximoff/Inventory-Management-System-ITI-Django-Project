from django.contrib import admin
from .models import Factory, Shipment, ShipmentItem


admin.site.register(Factory)
admin.site.register(Shipment)
admin.site.register(ShipmentItem)