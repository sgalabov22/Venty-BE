# Generated by Django 3.2.9 on 2022-02-07 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extensions', '0011_auto_20220207_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitems',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
