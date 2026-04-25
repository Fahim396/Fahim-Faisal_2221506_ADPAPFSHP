"""
Prediction and Report models.
Stores AI prediction results and generated reports.
"""

from django.db import models
from django.conf import settings


class Prediction(models.Model):
    """Stores pest prediction results linked to farm data."""

    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    farm_data = models.OneToOneField(
        'farmer.FarmData',
        on_delete=models.CASCADE,
        related_name='prediction'
    )
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES)
    confidence_score = models.FloatField(
        help_text='Confidence score between 0 and 1'
    )
    predicted_pest = models.CharField(max_length=100, blank=True, null=True)
    recommendation = models.TextField(
        help_text='Smart harvest recommendations'
    )
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text='Detailed prediction breakdown (JSON)'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'predictions'
        ordering = ['-created_at']
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return f"Prediction #{self.pk} - {self.get_risk_level_display()} Risk"

    @property
    def confidence_percent(self):
        return f"{self.confidence_score * 100:.1f}%"


class Report(models.Model):
    """Generated reports for analytics and monitoring."""

    REPORT_TYPE_CHOICES = [
        ('prediction_summary', 'Prediction Summary'),
        ('risk_analysis', 'Risk Analysis'),
        ('crop_report', 'Crop Report'),
        ('monthly_report', 'Monthly Report'),
    ]

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports'
    )
    content = models.JSONField(
        default=dict,
        help_text='Report data in JSON format'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"
