from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Event


class EventListView(ListView):
    queryset = Event.objects.all()
    context_object_name = 'events'
    paginate_by = 3
    template_name = 'events/list.html'
