from django.contrib import admin

# Register your models here.
from extensions.models import Checklist, ChecklistItems

admin.site.register(Checklist)
admin.site.register(ChecklistItems)