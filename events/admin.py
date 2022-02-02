from django.contrib import admin

# Register your models here.
from events.models import Event, Location, LocationPosition, LocationReview, Photos, WorkingHours


class EventsAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "start_date", "end_date",
                    "event_title", "description", "event_owner"]


admin.site.register(Event, EventsAdmin)
admin.site.register(Location)
admin.site.register(LocationPosition)
admin.site.register(LocationReview)
admin.site.register(Photos)
admin.site.register(WorkingHours)


