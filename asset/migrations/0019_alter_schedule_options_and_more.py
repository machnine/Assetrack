# Generated by Django 5.0.6 on 2024-08-06 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0018_alter_schedule_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['schedule_date'], 'verbose_name_plural': 'schedules'},
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='start_date',
            new_name='schedule_date',
        ),
    ]
