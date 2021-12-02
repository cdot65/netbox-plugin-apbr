from django.contrib import admin
from .models import Apbr


@admin.register(Apbr)
class ApbrAdmin(admin.ModelAdmin):
    fields = ('number', 'status', 'description')
