# Generated by Django 2.1.7 on 2019-03-22 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BUSINESS', '0005_auto_20190322_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='website',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='pin',
            field=models.IntegerField(default=2649),
        ),
    ]