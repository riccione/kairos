# Generated by Django 5.1 on 2024-08-30 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_rename_publish_event_published_event_periodicity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
