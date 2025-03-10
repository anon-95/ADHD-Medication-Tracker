# Generated by Django 5.1.6 on 2025-02-26 01:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_medication_profile_medication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='medication',
        ),
        migrations.AddField(
            model_name='profile',
            name='dosage',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='profile',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='Medication',
        ),
        migrations.AddField(
            model_name='profile',
            name='medication',
            field=models.CharField(default='not chosen', max_length=100),
        ),
    ]
