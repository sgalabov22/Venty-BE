# Generated by Django 3.2.9 on 2022-02-07 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_delete_extension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, help_text='Let your guest know details about this event', max_length=1000),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_title',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
