# Generated by Django 3.2.7 on 2021-09-25 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='lead_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='crf_pk',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
