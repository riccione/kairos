from django import forms
from .models import Event


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'creator',
            'event_date',
            'status',
        )
        widgets = {
            'event_date': forms.widgets.DateInput(attrs={'type': 'datetime-local'})
        }
