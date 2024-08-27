from django import forms
from .models import Event
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
)


User = get_user_model()

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"

class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N 
    # is True, the locale-dictated format will be applied 
    # instead of settings.DATETIME_INPUT_FORMATS.

    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        event_date = DateTimeLocalField()
        fields = (
            "name",
            "description",
            "event_date",
            "status",
        )
        widgets = {
                'event_date': DateTimeLocalInput(
                format='%Y-%m-%dT%H:%M'
                )
        }


class CustomUserCreationForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
