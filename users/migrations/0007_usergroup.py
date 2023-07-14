# Generated by Django 2.2.7 on 2019-11-14 12:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20191113_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('members', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, default=list, size=None)),
            ],
        ),
    ]