from dataclasses import fields
from django.contrib import admin
from .models import Ad, Comment


# Register your models here.
class AdAdmin(admin.ModelAdmin):
    exclude: list[str] = ["picture", "img_content_type"]


admin.site.register(Ad, AdAdmin)
admin.site.register(Comment)
