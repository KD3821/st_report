# Generated by Django 4.1 on 2022-08-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0006_extratax_alter_ride_extra_tax'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extratax',
            old_name='name',
            new_name='mode',
        ),
        migrations.AddField(
            model_name='ride',
            name='tax_result',
            field=models.IntegerField(default=0),
        ),
    ]
