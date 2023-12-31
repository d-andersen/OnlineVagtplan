# Generated by Django 2.2.7 on 2019-11-20 11:46

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_usergroup_group_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='group_type',
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='shifts',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='members',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='members',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, default=list, size=None),
        ),
    ]
