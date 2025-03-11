from django.db import models
from inventory.models import Product

# Create your models here.
class Factory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    
    def str(self):
        return self.name

class Shipment(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.RESTRICT, related_name="shipments")
    recieve_date = models.DateField()
    created_at = models.DateField(auto_now=True)
    confirmed = models.BooleanField(default=False)  # Only managers can confirm

    def __str__(self):
        return f"Shipment from {self.factory_name} on {self.date_received}"
    
class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.shipment.confirmed:  # Prevent modifications to confirmed shipments
            raise ValueError("Cannot modify a confirmed shipment")
        super().save(*args, **kwargs)
