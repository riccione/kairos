from django.shortcuts import reverse
from django.views import generic
from django.urls import reverse_lazy
from .models import Event
from .forms import EventModelForm, CustomUserCreationForm
from django.conf import settings

class LandingPageView(generic.TemplateView):
    template_name = "events/landing.html"

class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EventListView(generic.ListView):
    context_object_name = "events"
    paginate_by = settings.PAGINATION
    template_name = "events/list.html"

    def get_queryset(self):
        filter = self.kwargs.get("filter", "published")
        user = self.request.user
        if filter == "draft":
            queryset = Event.objects.filter(
                status__exact="draft",
                creator=user,
            )
        elif filter == "published":
            queryset = Event.objects.filter(
                status__exact="published",
                creator=user,
            )
        else:  # all
            queryset = Event.objects.filter(
                status__exact='published',
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.kwargs.get("filter", "published")
        return context

class EventPublicListView(generic.ListView):
    context_object_name = "events"
    paginate_by = settings.PAGINATION
    queryset = Event.objects.filter(
                status__exact="published",
            )
    template_name = "events/public_list.html"

class EventDetailView(generic.DetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/detail.html"

class EventPublicDetailView(generic.DetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/detail.html"

class EventCreateView(generic.CreateView):
    form_class = EventModelForm
    template_name = "events/create.html"

    def get_success_url(self):
        return reverse("events:event_list")

    def form_valid(self, form):
        event = form.save(commit=False)
        event.creator = self.request.user
        event.save()
        return super(EventCreateView, self).form_valid(form)


class EventUpdateView(generic.UpdateView):
    form_class = EventModelForm
    queryset = Event.objects.all()
    template_name = "events/update.html"
    success_url = reverse_lazy("events:event_list")


class EventDeleteView(generic.DeleteView):
    queryset = Event.objects.all()
    success_url = reverse_lazy("events:event_list")
    template_name = "events/delete.html"
