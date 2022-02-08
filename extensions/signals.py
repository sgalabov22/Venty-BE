from django.db.models.signals import post_save
from django.dispatch import receiver

from extensions.models import Checklist


@receiver(post_save, sender=Checklist)
def checklist_created(sender, instance, created, **kwargs):
    if created:
        instance["viewers"].append()

