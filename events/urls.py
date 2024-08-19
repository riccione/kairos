from django.urls import path
from .views import (
        EventListView,
        EventDetailView,
        EventCreateView,
        EventUpdateView,
        )

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
]
