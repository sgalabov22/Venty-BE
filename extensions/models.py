from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from events.models import Event
from users.models import Account


class ChecklistItems(models.Model):
    value = models.CharField(max_length=40, blank=True)
    def __str__(self):
        return f"{self.value}"

class Checklist(models.Model):
    items = models.ForeignKey(ChecklistItems, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    viewers = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.items}--------{self.event} ----{self.viewers}"
