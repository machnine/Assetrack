# Generated by Django 5.0.6 on 2024-06-24 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0007_software_source_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='software',
            options={'ordering': ['name']},
        ),
    ]
