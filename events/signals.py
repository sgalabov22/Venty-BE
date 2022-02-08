from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Event
from guests.models import Guest


@receiver(post_save, sender=Event)
def event_created(sender, instance, created, **kwargs):
    if created:
        guest = Guest()
        guest.guest_user_account_id = instance.event_owner.id
        guest.event_id = instance.id
        guest.save()

