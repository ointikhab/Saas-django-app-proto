# Generated by Django 4.2.20 on 2025-03-21 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_userprofile_is_organization_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_organization_admin',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='organization',
        ),
        migrations.CreateModel(
            name='UserOrganizationMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('employee', 'Employee')], default='employee', max_length=20)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'organization')},
            },
        ),
    ]
