# Generated by Django 5.0.6 on 2024-06-20 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0028_alter_category_options_alter_equipmenttype_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
