# Generated by Django 2.2.7 on 2019-11-17 13:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventplan', '0009_auto_20191117_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_attendees',
        ),
        migrations.AlterField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_type', models.CharField(choices=[(None, 'Choose shift type'), ('TS', 'Ticket Selling'), ('CS', 'Candy Selling'), ('MO', 'Movie Operation'), ('CL', 'Cleaning'), ('FS', 'Facility Service'), ('PR', 'PR Work')], max_length=2)),
                ('description', models.TextField(blank=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=datetime.datetime(2019, 11, 17, 14, 30, 25, 755302, tzinfo=utc))),
                ('volunteer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='shifts',
            field=models.ManyToManyField(blank=True, to='eventplan.Shift'),
        ),
    ]