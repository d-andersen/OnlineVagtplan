# Generated by Django 2.2.7 on 2019-11-20 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_usergroup_shifts'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='group_type',
            field=models.CharField(choices=[(None, 'Choose group type'), ('TS', 'Ticket Selling'), ('CS', 'Candy Selling'), ('MO', 'Movie Operation'), ('CL', 'Cleaning'), ('FS', 'Facility Service'), ('PR', 'PR Work'), ('OT', 'Other')], default='OT', max_length=2),
            preserve_default=False,
        ),
    ]
