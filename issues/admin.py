from django.contrib import admin
from .models import Status, Issue


# Register your models here.
class StatusAdmin(admin.ModelAdmin):
    list_display = [
        "name", "description"
    ]


admin.site.register(Status, StatusAdmin)
admin.site.register(Issue)