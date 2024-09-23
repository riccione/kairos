from django.shortcuts import reverse, render
from django.views import generic
from django.urls import reverse_lazy
from .models import Event, Ticket
from .forms import EventModelForm, CustomUserCreationForm
from django.conf import settings
import hashlib
from django.http import HttpResponseRedirect
from django.contrib import messages
from cities_light.models import City

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
                status__exact="published",
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

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        user = self.request.user

        h = hashlib.new("sha3_256")
        code = f"{event.id}_{user}_{settings.SECRET_KEY}"
        h.update(code.encode("utf-8"))
        code = h.hexdigest()
        active = True

        if Ticket.objects.filter(
            event=event,
            user=self.request.user,
        ).exists():
            messages.error(
                    self.request,
                    "You have already attended to the event")
            return HttpResponseRedirect(
                reverse_lazy("events:event_detail", kwargs={"pk": event.pk})
            )

        Ticket.objects.create(
            event=event,
            user=user,
            code=code,
            active=active,
        )

        # get current capacity
        capacity_actual = event.capacity_actual + 1

        event.capacity_actual = capacity_actual
        event.capacity_updated = True
        event.save()

        return HttpResponseRedirect(
            reverse_lazy("events:event_detail", kwargs={"pk": event.pk})
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        h = hashlib.new("sha3_256")
        crc = f"{event.id}_{settings.SECRET_KEY}"
        h.update(crc.encode("utf-8"))
        crc = h.hexdigest()
        context["crc"] = crc
        ticket = Ticket.objects.filter(
            user=self.request.user, event=self.get_object()
        ).last()
        context["ticket"] = ticket
        return context


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

    def form_valid(self, form):
        event = form.save(commit=False)
        new_capacity = form.cleaned_data.get('capacity')
        # print(event.capacity_updated, event.capacity_actual, new_capacity)
        if event.capacity_updated and event.capacity_actual > new_capacity:
            print(event.capacity_updated, event.capacity_actual, new_capacity)
            messages.error(
                    self.request,
                    "You can't change capacity below the actual capacity")
            return self.form_invalid(form)
        else:
            event.save()
            messages.success(
                    self.request,
                    "Event has been updated successfully")
        return super(EventUpdateView, self).form_valid(form)


class EventDeleteView(generic.DeleteView):
    queryset = Event.objects.all()
    success_url = reverse_lazy("events:event_list")
    template_name = "events/delete.html"


class TicketListView(generic.ListView):
    context_object_name = "tickets"
    paginate_by = settings.PAGINATION
    template_name = "events/ticket_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(
            user=self.request.user
        )
        return queryset


class TicketDetailView(generic.DetailView):
    model = Ticket
    context_object_name = "ticket"
    template_name = "events/ticket_detail.html"

# test url
# http://127.0.0.1:8000/events/load_cities/?country=35
def load_cities(request):
    country_id = request.GET.get("country")
    cities = City.objects.filter(country_id=country_id)
    return render(request, "events/city_options.html", {"cities": cities})
