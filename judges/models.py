from django.db import models
from users.models import User
from events.models import Event

class Judge(User):
    access_code = models.CharField(max_length=50, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="judges")
    specialization = models.CharField(max_length=100)
    image = models.TextField(blank=True, null=True)

 
    def __str__(self):
        return f"{self.name} (Judge)"
    
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(check=~models.Q(email__exact=''), name='judge_email_not_empty'),
    #     ]