from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, Ticket


admin.site.register(User, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ("status", "created", "creator", "event_date")


admin.site.register(Ticket)
