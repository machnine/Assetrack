# Generated by Django 5.0.6 on 2024-06-24 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_alter_software_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='last_updated',
            new_name='last_updated_at',
        ),
    ]