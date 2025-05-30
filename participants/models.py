from django.db import models

# Create your models here.
from django.db import models
from events.models import Event
from categories.models import Category

class Participant(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    entry = models.TextField()
    registration_date = models.DateTimeField()
    contestant_number = models.PositiveIntegerField()
    email = models.EmailField()
    origin = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[
        ("Male", "Male"),
        ("Female", "Female"),
    ])
    image = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.name} (Contestant #{self.contestant_number})"