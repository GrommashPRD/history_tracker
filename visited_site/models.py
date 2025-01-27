from django.db import models
from django.utils import timezone


# Create your models here.
class VisitedLink(models.Model):
    url = models.URLField(unique=True)  # URL должен быть уникальным
    timestamp = models.DateField(default=timezone.now)

    def __str__(self):
        return self.url
