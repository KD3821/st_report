# Generated by Django 4.1 on 2022-08-13 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='tip',
            field=models.IntegerField(default=0),
        ),
    ]
