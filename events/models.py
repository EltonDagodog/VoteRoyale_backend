from django.db import models
from coordinators.models import Coordinator

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ("upcoming", "Upcoming"),
        ("open", "Open"),
        ("closed", "Closed"),
    ])
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField()
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE, related_name="events")

    def __str__(self):
        return self.title