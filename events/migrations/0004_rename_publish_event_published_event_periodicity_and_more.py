# Generated by Django 5.1 on 2024-08-30 03:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_rename_descrption_event_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="publish",
            new_name="published",
        ),
        migrations.AddField(
            model_name="event",
            name="periodicity",
            field=models.CharField(
                choices=[
                    ("none", "None"),
                    ("daily", "Daily"),
                    ("weekly", "Weekly"),
                    ("monthly", "Monthly"),
                    ("annually", "Annually"),
                ],
                default="none",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=250)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("used", models.DateTimeField()),
                ("active", models.BooleanField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket",
                        to="events.event",
                    ),
                ),
            ],
        ),
    ]
