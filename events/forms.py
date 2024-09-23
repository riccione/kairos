from django import forms
from .models import Event
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
)
from cities_light.models import City


User = get_user_model()


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N
    # is True, the locale-dictated format will be applied
    # instead of settings.DATETIME_INPUT_FORMATS.

    input_formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M"]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        event_date = DateTimeLocalField()
        fields = (
            "name",
            "description",
            "event_date",
            "event_time",
            "periodicity",
            "status",
            "capacity",
            "country",
            "city",
        )
        widgets = {
            #"event_date": DateTimeLocalInput(format="%Y-%m-%d"),
            "event_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}),
            #"event_time": DateTimeLocalInput(format="%H:%M"),
            "event_time": forms.TimeInput(
                format="%H:%M",
                attrs={'type': 'time'}),
            "country": forms.Select(attrs={
                "hx-get": "/events/load_cities/",
                "hx-target":"#id_city"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for UpdateView, ?self.instance.pk
        if self.instance:
            country_id = self.instance.country
            self.fields['city'].queryset = City.objects.filter(
                country_id=country_id
            )
        else:
            self.fields['city'].queryset = City.objects.none()

        # for CreateView
        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["city"].queryset = City.objects.filter(
                        country_id=country_id
                )
            except (ValueError, TypeError):
                self.fields['city'].queryset = City.objects.none()


class CustomUserCreationForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
