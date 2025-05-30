from django.db import models
from django.core.validators import MinValueValidator
from events.models import Event

class Category(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="categories")
    description = models.TextField()
    max_score = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=[
        ("open", "Open"),
        ("closed", "Closed"),
    ])
    gender = models.CharField(max_length=10, choices=[
        ("male", "Male"),
        ("female", "Female"),
        ("everyone", "Everyone"),
    ])
    award_type = models.CharField(max_length=10, choices=[
        ("major", "Major"),
        ("minor", "Minor"),
    ], default="major")  # Default to "major" for existing records

    def __str__(self):
        return f"{self.name} ({self.event.title})"