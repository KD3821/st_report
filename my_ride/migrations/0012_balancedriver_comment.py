# Generated by Django 4.1 on 2022-08-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0011_balancedriver'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancedriver',
            name='comment',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
