# Generated by Django 5.0.6 on 2024-08-18 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0035_alter_maintenancerecordassignment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceRecordMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_icon', models.CharField(max_length=50)),
                ('link_text', models.CharField(max_length=50)),
                ('equipment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.equipmenttype')),
            ],
        ),
    ]
