# Generated by Django 3.2.9 on 2022-02-05 14:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extensions', '0007_auto_20220205_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='viewers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
