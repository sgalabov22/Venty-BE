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


def event_guests(pk):
    guests = [guest_event.guest_user_account for guest_event in Guest.objects.filter(event=pk)]
    return guests


def event_guest_emails(pk):
    guest_emails = [record.guest_user_account.email for record in Guest.objects.filter(event=pk)]
    return guest_emails


def checklist_viewers_emails(pk, ext_id):
    viewers_emails = [record.email for record in Checklist.objects.get(event=pk, id=ext_id).viewers.all()]
    return viewers_emails


def reminder_viewers_emails(pk, ext_id):
    viewers_emails = [record.email for record in Reminder.objects.get(event=pk, id=ext_id).viewers.all()]
    return viewers_emails


def viewers(pk, ext_id, current_viewers):
    available_viewers = [viewer for viewer in event_guests(pk) if
                         viewer not in current_viewers(pk, ext_id)]
    return available_viewers
