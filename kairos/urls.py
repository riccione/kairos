from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_not_required
from events.views import LandingPageView

urlpatterns = [
    path('', login_not_required(LandingPageView.as_view()), name='landing'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls', namespace='events')),
]
