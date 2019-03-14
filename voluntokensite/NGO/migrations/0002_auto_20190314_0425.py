# Generated by Django 2.1.7 on 2019-03-14 04:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NGO', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_registration_stub',
            name='parent_volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='parent_ngo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NGO.org'),
        ),
        migrations.AddField(
            model_name='checks_stub',
            name='parent_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NGO.event'),
        ),
        migrations.AddField(
            model_name='checks_stub',
            name='parent_volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]