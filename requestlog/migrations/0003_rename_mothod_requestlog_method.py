# Generated by Django 5.0.6 on 2024-07-04 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requestlog', '0002_alter_requestlog_status_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestlog',
            old_name='mothod',
            new_name='method',
        ),
    ]