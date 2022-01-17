from django.db import models
from django.utils import timezone

# Create your models here.
from users.models import Account


class Guest(models.Model):
    STATUS_TYPES = (
        ('attending', 'attending'),
        ('declined', 'declined'),
    )

    guest_user_account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default='attending')

    def __str__(self):
        return f"{self.guest_user_account} {self.status}"

class Extensions(models.Model):
    EXTENSIONS_TYPE = (
        ('checklist', 'checklist'),
        ('', '')
    )
    extensions_type = models.CharField(max_length=10, choices=EXTENSIONS_TYPE, default='')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.extensions_type} {self.is_liked}"

#TODO to fixed the bug with modified_at data It is not chanble after an update
class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now, editable=False)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    end_date = models.DateTimeField(null=True, blank=True, default=None)

    event_title = models.CharField(max_length=30)

    goal = models.CharField(max_length=300, blank=True)
    agenda = models.TextField(max_length=1000, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    location_id = models.CharField(max_length=40)

    event_owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    guests = models.ManyToManyField(Guest, blank=True)
    extensions = models.ManyToManyField(Extensions, blank=True)
