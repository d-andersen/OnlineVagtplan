# Generated by Django 2.2.7 on 2019-11-20 11:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20191120_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='users',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='group_type',
            field=models.CharField(choices=[(None, 'Choose group type'), ('TS', 'Ticket Selling'), ('CS', 'Candy Selling'), ('MO', 'Movie Operation'), ('CL', 'Cleaning'), ('FS', 'Facility Service'), ('PR', 'PR Work'), ('OT', 'Other')], default='OT', max_length=2),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='members',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
