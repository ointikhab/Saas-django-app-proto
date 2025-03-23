# Generated by Django 4.2.20 on 2025-03-22 11:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_user',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_users',
            field=models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
