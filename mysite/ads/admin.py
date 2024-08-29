from dataclasses import fields
from django.contrib import admin
from .models import Ad


# Register your models here.
class AdAdmin(admin.ModelAdmin):
    exclude: list[str] = ["img", "img_content_type"]


admin.site.register(Ad, AdAdmin)
