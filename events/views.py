from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import Event
from .forms import EventModelForm


class LandingPageView(generic.TemplateView):
    template_name = 'events/landing.html'

class EventListView(generic.ListView):
    queryset = Event.objects.all()
    context_object_name = 'events'
    paginate_by = 3
    template_name = 'events/list.html'

    def get_queryset(self):
        return Event.objects.filter(status__exact='published')

class EventDetailView(generic.DetailView):
    model = Event
    context_object_name = 'events'
    template_name = 'events/detail.html'

class EventCreateView(generic.CreateView):
    form_class = EventModelForm
    success_url = 'events/'
    template_name = 'events/create.html'

    def form_valid(self, form):
        event = form.save()
        return super(EventCreateView, self).form_valid(form)
