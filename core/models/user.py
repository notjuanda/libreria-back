from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ci = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
