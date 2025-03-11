from django.contrib import admin
from .models import Supermarket, Order, OrderItem


admin.site.register(Supermarket)
admin.site.register(Order)
admin.site.register(OrderItem)