# Generated by Django 5.0.6 on 2024-07-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0010_alter_equipment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
