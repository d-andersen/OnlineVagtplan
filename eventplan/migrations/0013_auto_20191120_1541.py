# Generated by Django 2.2.7 on 2019-11-20 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventplan', '0012_auto_20191120_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='shifts',
            field=models.ManyToManyField(blank=True, related_name='events', to='eventplan.Shift'),
        ),
    ]
