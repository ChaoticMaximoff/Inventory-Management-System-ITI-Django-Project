from django.db import models
from inventory.models import Product
from django.conf import settings


class Supermarket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    ]

    supermarket = models.ForeignKey(Supermarket, on_delete=models.RESTRICT, related_name="orders")
    created_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )


    def str(self):
        return f"Order to {self.supermarket.name} - {self.status}"
    
    def __str__(self):
        return str(self.id)
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )

    def save(self, *args, **kwargs):
        if self.order.status == Order.CONFIRMED:  # Prevent modifications to confirmed orders
            raise ValueError("Cannot modify a confirmed order")
        if self.quantity > self.product.quantity:
            raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order: {self.order.id})"