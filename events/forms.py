from django import forms
from .models import Event
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
)


User = get_user_model()


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "event_date",
            "status",
        )
        widgets = {
            "event_date": forms.widgets.DateInput(attrs={"type": "datetime-local"})
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
