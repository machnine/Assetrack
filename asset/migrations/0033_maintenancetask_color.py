# Generated by Django 5.0.6 on 2024-08-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0032_equipmenttype_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancetask',
            name='color',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]
