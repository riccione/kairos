from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_date(x):
    if x < timezone.now().date():
        raise ValidationError("Date cannot be in the past")


class User(AbstractUser):
    pass


class Event(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    PERIODICITY_CHOICES = (
        ("none", "None"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("annually", "Annually"),
    )
    name = models.CharField(max_length=250)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event")
    event_date = models.DateField(validators=[validate_date])
    event_time = models.TimeField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    periodicity = models.CharField(
        max_length=20, choices=PERIODICITY_CHOICES, default="none"
    )
    capacity = models.IntegerField(default=50)
    capacity_actual = models.IntegerField(default=0)
    capacity_updated = models.BooleanField(default=False)
    country = models.ForeignKey('cities_light.Country',
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    city = models.ForeignKey('cities_light.City',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)

    class Meta:
        ordering = ("event_date",)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    code = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    used = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.code
