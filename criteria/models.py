from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from categories.models import Category

class Criterion(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="criteria")
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage weight of this criterion (0-100)"
    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"