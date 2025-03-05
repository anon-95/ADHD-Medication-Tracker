# Generated by Django 5.1.6 on 2025-03-01 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_journal_day_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='mood',
            field=models.CharField(choices=[('Stable', 'Stable'), ('Improving', 'Improving'), ('Worsening', 'Worsening')], default='Stable', max_length=50),
        ),
    ]
