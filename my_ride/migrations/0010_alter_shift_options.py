# Generated by Django 4.1 on 2022-08-17 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0009_alter_ride_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ['date']},
        ),
    ]
