# Generated by Django 2.1.7 on 2019-03-22 04:07

import NGO.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='checks_stub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_check_in', models.BooleanField(default=True)),
                ('time', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2500)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to=NGO.models.get_image_path)),
                ('pin_checkin', models.IntegerField(default=7380)),
                ('pin_checkout', models.IntegerField(default=7675)),
                ('is_active', models.BooleanField(default=True)),
                ('volunteer_hour', models.FloatField(default=0.0)),
                ('start_time', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('end_time', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.CreateModel(
            name='event_hours_spent_stub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='event_registration_stub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NGO.event')),
            ],
        ),
        migrations.CreateModel(
            name='org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2500)),
                ('email', models.EmailField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('volunteer_hour', models.FloatField(default=0.0)),
            ],
        ),
    ]
