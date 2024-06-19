# Generated by Django 5.0.6 on 2024-06-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0013_alter_equipment_options_alter_recordtype_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='replacement_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='value',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]