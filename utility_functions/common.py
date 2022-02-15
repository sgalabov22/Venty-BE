from extensions.models import Checklist, Reminder
from guests.models import Guest


def current_checklist_viewers(pk, ext_id):
    viewers = [viewers for checklist in Checklist.objects.filter(event=pk, id=ext_id) for viewers
               in checklist.viewers.all()]
    return viewers


def current_reminder_viewers(pk, ext_id):
    viewers = [viewers for reminder in Reminder.objects.filter(event=pk, id=ext_id) for viewers in
               reminder.viewers.all()]
    return viewers


def guests(pk):
    guests = Guest.objects.filter(event_id=pk)
    list_guests = [guest.guest_user_account for guest in guests]
    return list_guests


def event_guests(pk):
    guests = [guest_event.guest_user_account_id for guest_event in Guest.objects.filter(event=pk)]
    return guests