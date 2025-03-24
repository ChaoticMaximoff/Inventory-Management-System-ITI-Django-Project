from django.db import models

class Product(models.Model):
    image = models.ImageField(upload_to='blog/%Y/%m/%d')
    name = models.CharField(max_length=255, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    critical_level = models.PositiveIntegerField(default=10)  # Alert if stock < critical_level

    def is_low_stock(self):
        return self.quantity < self.critical_level
    
    def __str__(self):
        return f"{self.name} ({self.quantity} in stock)"