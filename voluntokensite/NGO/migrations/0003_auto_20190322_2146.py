# Generated by Django 2.1.7 on 2019-03-22 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0002_auto_20190322_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='pin_checkin',
            field=models.IntegerField(default=4272),
        ),
        migrations.AlterField(
            model_name='event',
            name='pin_checkout',
            field=models.IntegerField(default=7600),
        ),
    ]
