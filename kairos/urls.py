from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_not_required
from events.views import LandingPageView, SignupView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
)

urlpatterns = [
    path('', login_not_required(LandingPageView.as_view()), name='landing'),
    path('login/', login_not_required(LoginView.as_view()), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', login_not_required(SignupView.as_view()), name='signup'),
    path('reset-password/',
         login_not_required(PasswordResetView.as_view()),
         name='reset_password'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls', namespace='events')),
]
