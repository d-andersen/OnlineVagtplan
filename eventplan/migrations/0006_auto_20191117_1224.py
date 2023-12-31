# Generated by Django 2.2.7 on 2019-11-17 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventplan', '0005_auto_20191116_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={},
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_attendees',
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_type', models.CharField(choices=[(None, 'Choose shift type'), ('TS', 'Ticket Selling'), ('CS', 'Candy Selling'), ('MO', 'Movie Operation'), ('CL', 'Cleaning'), ('FS', 'Facility Service'), ('PR', 'PR Work')], max_length=2)),
                ('volunteer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='shifts',
            field=models.ManyToManyField(to='eventplan.Shift'),
        ),
    ]
