from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from judges.models import Judge
from participants.models import Participant
from categories.models import Category
from events.models import Event

class Vote(models.Model):
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name="votes")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="votes")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="votes")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="votes")
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField()

    def __str__(self):
        return f"Vote by {self.judge.name} for {self.participant.name} in {self.category.name}"