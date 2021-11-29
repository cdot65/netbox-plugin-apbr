from django.contrib import admin
from .models import ApbrProfile


@admin.register(ApbrProfile)
class ApbrProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "smell")
