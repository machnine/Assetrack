# Generated by Django 5.0.6 on 2024-07-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requestlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestlog',
            name='status_code',
            field=models.IntegerField(null=True),
        ),
    ]
