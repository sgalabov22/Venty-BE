from django.db import models
from django.utils import timezone

# Create your models here.
from users.models import Account


class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
    event_title = models.CharField(max_length=30, default=None)
    description = models.TextField(max_length=1000, blank=True,
                                   help_text="Let your guest know details about this event")
    event_owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    location = models.CharField(max_length=60, default=None)

    def __str__(self):
        return f"{self.event_title}"
