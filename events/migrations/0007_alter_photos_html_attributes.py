# Generated by Django 3.2.9 on 2022-02-02 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20220202_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='html_attributes',
            field=models.CharField(blank=True, default=None, max_length=200),
        ),
    ]
