# Generated by Django 5.0.6 on 2024-06-05 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0015_alter_equipment_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentattachment',
            options={'ordering': ['-uploaded_at']},
        ),
    ]