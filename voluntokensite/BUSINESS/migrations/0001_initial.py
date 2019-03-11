# Generated by Django 2.1.7 on 2019-03-11 21:05

import BUSINESS.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2500)),
                ('email', models.EmailField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('donation_tokens', models.FloatField()),
                ('discount_tokens', models.FloatField()),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to=BUSINESS.models.get_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('is_donation', models.BooleanField(default=True)),
                ('token_cost', models.FloatField(default=0.0)),
                ('donation_val', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='transaction_stub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_donation', models.BooleanField(default=True)),
                ('tokens_transferred', models.FloatField(default=0.0)),
                ('parent_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BUSINESS.business')),
            ],
        ),
    ]
