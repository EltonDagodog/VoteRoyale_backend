# Create your models here.
from django.db import models
from users.models import User

class Coordinator(User):
    department = models.CharField(max_length=100, default="Event Management")

    def __str__(self):
        return f"{self.name} (Coordinator)"