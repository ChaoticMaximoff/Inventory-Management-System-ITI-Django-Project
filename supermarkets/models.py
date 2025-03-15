from django.db import models


class Supermarket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def str(self):
        return self.name
