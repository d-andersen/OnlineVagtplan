# Generated by Django 2.2.7 on 2019-11-17 11:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eventplan', '0006_auto_20191117_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start',
        ),
        migrations.AddField(
            model_name='shift',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='end',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shift',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='shifts',
            field=models.ManyToManyField(blank=True, to='eventplan.Shift'),
        ),
    ]