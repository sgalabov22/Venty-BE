from django.db.models.signals import post_save
from django.dispatch import receiver
from extensions.models import Reminder
from jobs.updater import start


@receiver(post_save, sender=Reminder)
def list_reminders_updated(sender, instance, created, **kwargs):
    print("signals - reminder-created")
    start()

