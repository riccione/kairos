# Generated by Django 5.1 on 2024-08-30 03:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0005_event_capacity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="capacity",
            field=models.IntegerField(default=50),
        ),
    ]
