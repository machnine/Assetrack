# Generated by Django 5.0.6 on 2024-07-30 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0013_rename_assetschedule_schedule_alter_schedule_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='added_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='added_user',
            new_name='created_by',
        ),
    ]