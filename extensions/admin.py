from django.contrib import admin

# Register your models here.
from extensions.models import Checklist, ChecklistItems, Reminder

admin.site.register(Checklist)
admin.site.register(ChecklistItems)
admin.site.register(Reminder)
