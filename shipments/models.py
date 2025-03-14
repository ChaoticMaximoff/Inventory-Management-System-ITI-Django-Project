from django.db import models
from django.forms import ValidationError
from factories.models import Factory
from inventory.models import Product
from django.conf import settings


class Shipment(models.Model):
    factory = models.ForeignKey(
        Factory, on_delete=models.RESTRICT, related_name="shipments"
    )
    receive_date = models.DateField()
    created_at = models.DateField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipments",
    )

    def __str__(self):
        return f"Shipment from {self.factory.name} on {self.receive_date}"


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipment_items",
    )

    def save(self, *args, **kwargs):
        if self.shipment.confirmed:
            raise ValidationError("Cannot modify a confirmed shipment")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Shipment {self.shipment.id})"
