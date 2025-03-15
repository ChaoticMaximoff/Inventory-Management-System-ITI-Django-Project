from django.db import models
from inventory.models import Product
from supermarkets.models import Supermarket


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
    created_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def str(self):
        return f"Order to {self.supermarket.name} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if (
            self.order.status == Order.CONFIRMED
        ):  # Prevent modifications to confirmed orders
            raise ValueError("Cannot modify a confirmed order")
        if self.quantity > self.product.quantity:
            raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)
