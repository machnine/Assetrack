# Generated by Django 5.0.6 on 2024-06-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0008_alter_software_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
