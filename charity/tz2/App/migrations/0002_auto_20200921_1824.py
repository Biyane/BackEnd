# Generated by Django 3.1.1 on 2020-09-21 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(max_length=11),
        ),
    ]
