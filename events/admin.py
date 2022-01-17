from django.contrib import admin

# Register your models here.
from events.models import Event, Guest, Extensions


class EventsAdmin(admin.ModelAdmin):
    list_display = ["created_at", "modified_at", "start_date", "end_date",
                    "event_title", "goal", "agenda", "description",
                    "location_id", "event_owner"]


admin.site.register(Event, EventsAdmin)
admin.site.register(Guest)
admin.site.register(Extensions)
