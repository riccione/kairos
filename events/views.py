from django.shortcuts import render, reverse
from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from .models import Event
from .forms import EventModelForm, CustomUserCreationForm


class LandingPageView(generic.TemplateView):
    template_name = 'events/landing.html'

class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

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
    template_name = 'events/create.html'

    def get_success_url(self):
        return reverse('events:event_list')

    def form_valid(self, form):
        event = form.save()
        return super(EventCreateView, self).form_valid(form)

class EventUpdateView(generic.UpdateView):
    form_class = EventModelForm
    queryset = Event.objects.all()
    template_name = 'events/update.html'
    success_url = reverse_lazy('events:event_list')

class EventDeleteView(generic.DeleteView):
    queryset = Event.objects.all()
    success_url = reverse_lazy('events:event_list')
    template_name = 'events/delete.html'
