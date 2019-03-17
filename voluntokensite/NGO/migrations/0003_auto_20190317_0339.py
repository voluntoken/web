# Generated by Django 2.1.7 on 2019-03-17 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0002_auto_20190315_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='volunteer_hour',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='event',
            name='pin_checkin',
            field=models.IntegerField(default=1664),
        ),
        migrations.AlterField(
            model_name='event',
            name='pin_checkout',
            field=models.IntegerField(default=1394),
        ),
    ]