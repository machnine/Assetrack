# Generated by Django 5.0.6 on 2024-07-30 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0014_rename_added_date_schedule_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]