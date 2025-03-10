from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    EMPLOYEE = 'EMPLOYEE'
    MANAGER = 'MANAGER'

    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (MANAGER, 'Manager'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=EMPLOYEE)
