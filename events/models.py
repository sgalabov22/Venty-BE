from django.db import models
from django.utils import timezone

# Create your models here.
from users.models import Account



class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
    event_title = models.CharField(max_length=30, default=None)
    goal = models.CharField(max_length=300, blank=True)
    agenda = models.TextField(max_length=1000, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    location_id = models.CharField(max_length=40, default=None)

    event_owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event_title}"


class Guest(models.Model):
    STATUS_TYPES = (
        ('attending', 'attending'),
        ('declined', 'declined'),
    )

    guest_user_account = models.ForeignKey(Account, on_delete=models.CASCADE, unique=False)
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='attending')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.guest_user_account}--{self.status} --- Event - {self.event.id}"


class Extensions(models.Model):
    EXTENSIONS_TYPE = (
        ('checklist', 'checklist'),
        ('', '')
    )
    extensions_name = models.CharField(max_length=30, default=None)
    extensions_type = models.CharField(max_length=10, choices=EXTENSIONS_TYPE, default='')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.extensions_name}--{self.extensions_type}--{self.is_liked}"
