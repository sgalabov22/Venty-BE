# Generated by Django 3.2.9 on 2022-02-05 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extensions', '0004_reminder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminder',
            old_name='email_text',
            new_name='email_body',
        ),
        migrations.RenameField(
            model_name='reminder',
            old_name='scheduling',
            new_name='scheduled',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='event',
        ),
    ]
