# Generated by Django 4.1 on 2022-09-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0012_balancedriver_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancedriver',
            name='mileage',
            field=models.IntegerField(default=0),
        ),
    ]