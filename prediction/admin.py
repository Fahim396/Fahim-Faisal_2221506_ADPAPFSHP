from django.contrib import admin
from .models import Prediction, Report


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'farm_data', 'risk_level', 'confidence_score', 'predicted_pest', 'created_at')
    list_filter = ('risk_level',)
    search_fields = ('predicted_pest', 'farm_data__user__username')
    ordering = ('-created_at',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'created_at')
    list_filter = ('report_type',)
    ordering = ('-created_at',)
