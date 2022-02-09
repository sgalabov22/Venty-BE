from django.db import models
from events.models import Event
from users.models import Account


class ChecklistItems(models.Model):
    value = models.CharField(max_length=40, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.value}"


class Checklist(models.Model):
    name = models.CharField(max_length=30, default=None)
    items = models.ManyToManyField(ChecklistItems)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    viewers = models.ManyToManyField(Account)

    def __str__(self):
        return f"{self.items}"


class Reminder(models.Model):
    name = models.CharField(max_length=30, default=None)
    scheduled = models.DateTimeField(null=True, blank=True, default=None)
    email_body = models.TextField(blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    viewers = models.ManyToManyField(Account)
