# Generated by Django 3.2.9 on 2022-02-02 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20220202_1252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event',
            new_name='location',
        ),
    ]
