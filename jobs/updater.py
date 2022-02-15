from django.utils import timezone
import tzlocal

from apscheduler.schedulers.background import BackgroundScheduler
from extensions.models import Reminder
from jobs.jobs_reminders import send_reminder
from venty.settings import EMAIL_HOST_USER

scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
scheduler.start()

def start():
    list_jobs = scheduler.get_jobs()
    if list_jobs:
        for job in list_jobs:
            job.remove()

    reminders = Reminder.objects.all()
    for reminder in reminders:

        subject = f'Reminder from Venty about {reminder.event.event_title} - {reminder.name}.'
        list_subscribers = [viewer.email for viewer in reminder.viewers.all()]
        current_datetime = timezone.now()

        if current_datetime <= reminder.scheduled:

            scheduler.add_job(send_reminder, 'date', run_date=reminder.scheduled, args=[
                subject,
                reminder.email_body,
                EMAIL_HOST_USER,
                list_subscribers,
            ])