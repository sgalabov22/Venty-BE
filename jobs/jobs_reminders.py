
from django.core.mail import send_mail




def send_reminder(subject,email_body,email_from,list_subscribers):
    print("email is sent")
    send_mail(
        subject,
        email_body,
        email_from,
        list_subscribers
    )
