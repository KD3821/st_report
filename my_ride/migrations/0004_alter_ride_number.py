# Generated by Django 4.1 on 2022-08-13 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0003_alter_ride_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
