from django.db import models
from inventory.models import Product
from supermarkets.models import Supermarket
from django.conf import settings
from django.core.validators import MinValueValidator


class Order(models.Model):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
    ]

    supermarket = models.ForeignKey(
        Supermarket, on_delete=models.RESTRICT, related_name="orders"
    )
    receive_date = models.DateField()
    created_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    def __str__(self):
        return f"Order to {self.supermarket.name} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField()
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )

    def save(self, *args, **kwargs):
        if (
            self.order.status == Order.CONFIRMED
        ):  # Prevent modifications to confirmed orders
            raise ValueError("Cannot modify a confirmed order")
        if self.quantity > self.product.quantity:
            raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order: {self.order.id})"
    def __str__(self):
        return str(self.id)