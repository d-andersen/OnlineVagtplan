# Generated by Django 2.2.7 on 2019-11-15 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20191115_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birth_date',
        ),
    ]
