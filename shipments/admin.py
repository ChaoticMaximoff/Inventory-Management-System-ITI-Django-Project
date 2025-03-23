from django.contrib import admin
from .models import Shipment, ShipmentItem


admin.site.register(Shipment)
admin.site.register(ShipmentItem)
