# Generated by Django 2.1.7 on 2019-03-22 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BUSINESS', '0007_auto_20190322_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='total_support_stub',
            name='total_transactions',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AlterField(
            model_name='business',
            name='pin',
            field=models.IntegerField(default=5838),
        ),
    ]