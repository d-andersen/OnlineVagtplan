# Generated by Django 2.2.7 on 2019-11-16 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventplan', '0004_auto_20191114_1328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start']},
        ),
        migrations.RemoveField(
            model_name='event',
            name='created_by',
        ),
    ]