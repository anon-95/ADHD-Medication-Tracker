# Generated by Django 5.1.6 on 2025-03-04 00:41

import tracker.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_rename_remembered_medication_journal_remembered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date_posted',
            field=models.DateTimeField(default=tracker.models.get_current_local_time),
        ),
    ]
