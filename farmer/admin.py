from django.contrib import admin
from .models import FarmData, Alert


@admin.register(FarmData)
class FarmDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop_type', 'soil_condition', 'weather', 'planting_date', 'created_at')
    list_filter = ('crop_type', 'soil_condition', 'weather')
    search_fields = ('user__username', 'crop_type')
    ordering = ('-created_at',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'severity', 'is_read', 'created_at')
    list_filter = ('severity', 'is_read')
    search_fields = ('user__username', 'title')
    ordering = ('-created_at',)
