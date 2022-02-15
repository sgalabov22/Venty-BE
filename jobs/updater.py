from django.utils import timezone
import tzlocal

from apscheduler.schedulers.background import BackgroundScheduler
from extensions.models import Reminder
from jobs.jobs_reminders import send_reminder
from venty.settings import EMAIL_HOST_USER

scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
scheduler.start()

def start():
    print("start-function-list reminders up to date ")
    list_jobs = scheduler.get_jobs()
    print(f"before_the_loop:{list_jobs}")

    if list_jobs:
        for job in list_jobs:
            job.remove()
    print(f"before_the_loop:{scheduler.get_jobs()}")
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
            list_jobs = scheduler.get_jobs()
            print(f"List of jobs after rescheduling: {list_jobs}")

            # scheduler.shutdown()
