from django.contrib import admin

from .models import CustomField
from .custom_field import CustomFieldAdmin


class CFAdmin(CustomFieldAdmin):
    list_display = ("content_type", "name")
    list_filter = ("content_type",)
    search_fields = ("content_type__name", "name")


admin.site.register(CustomField, CFAdmin)
