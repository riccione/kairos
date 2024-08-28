from django.urls import path
from django.contrib.auth.decorators import login_not_required
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventPublicDetailView,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("create/", EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("public/<int:pk>/", login_not_required(EventPublicDetailView.as_view()),
         name="event_public_detail"),
    path("<int:pk>/update/", EventUpdateView.as_view(), name="event_update"),
    path("<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
    path("<str:filter>/", EventListView.as_view(), name="event_list_filtered"),
]
