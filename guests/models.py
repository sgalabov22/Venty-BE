from django.db import models

# Create your models here.
from events.models import Event
from users.models import Account


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

