# Generated by Django 2.1.7 on 2019-03-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_total_hours_stub_total_donation_tokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='total_hours_stub',
            name='total_discount_tokens',
            field=models.FloatField(default=0.0),
        ),
    ]
