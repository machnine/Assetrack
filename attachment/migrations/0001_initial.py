# Generated by Django 5.0.6 on 2024-08-08 10:56

import attachment.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=attachment.models.UploadToPathAndRename('attachments'), verbose_name='file')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='uploaded at')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_attachments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'abstract': False,
            },
        ),
    ]