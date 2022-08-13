# Generated by Django 4.1 on 2022-08-13 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_ride', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='owns',
            new_name='deposit',
        ),
        migrations.RemoveField(
            model_name='car',
            name='date',
        ),
        migrations.RemoveField(
            model_name='car',
            name='fix',
        ),
        migrations.RemoveField(
            model_name='car',
            name='fuel',
        ),
        migrations.RemoveField(
            model_name='car',
            name='income',
        ),
        migrations.RemoveField(
            model_name='car',
            name='other',
        ),
        migrations.RemoveField(
            model_name='car',
            name='rides',
        ),
        migrations.RemoveField(
            model_name='car',
            name='service',
        ),
        migrations.RemoveField(
            model_name='car',
            name='wash',
        ),
        migrations.AddField(
            model_name='car',
            name='rental_rate',
            field=models.IntegerField(default=3000),
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel', models.IntegerField(default=0)),
                ('wash', models.IntegerField(default=0)),
                ('service', models.IntegerField(default=0)),
                ('repair', models.IntegerField(default=0)),
                ('other', models.IntegerField(default=0)),
                ('income', models.IntegerField(default=0)),
                ('s_tax', models.IntegerField(default=0)),
                ('x_tax', models.IntegerField(default=0)),
                ('salary', models.IntegerField(default=0)),
                ('note', models.CharField(max_length=200)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_ride.car')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_ride.shift')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_ride.driver')),
            ],
        ),
    ]