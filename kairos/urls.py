from django.contrib import admin
from django.urls import path, include
from events.views import LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls', namespace='events')),
]
