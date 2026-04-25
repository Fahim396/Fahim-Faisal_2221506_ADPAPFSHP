"""
Farmer module models: FarmData and Alert.
Normalized schema with foreign keys and timestamps.
"""

from django.db import models
from django.conf import settings


class FarmData(models.Model):
    """Stores farm data entries submitted by farmers."""

    CROP_CHOICES = [
        ('rice', 'Rice'),
        ('wheat', 'Wheat'),
        ('corn', 'Corn'),
        ('cotton', 'Cotton'),
        ('sugarcane', 'Sugarcane'),
        ('potato', 'Potato'),
        ('tomato', 'Tomato'),
        ('soybean', 'Soybean'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('other', 'Other'),
    ]

    SOIL_CHOICES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silt', 'Silt'),
        ('peat', 'Peat'),
        ('chalk', 'Chalk'),
        ('other', 'Other'),
    ]

    WEATHER_CHOICES = [
        ('sunny', 'Sunny'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
        ('humid', 'Humid'),
        ('dry', 'Dry'),
        ('windy', 'Windy'),
        ('stormy', 'Stormy'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farm_data'
    )
    crop_type = models.CharField(max_length=50, choices=CROP_CHOICES)
    soil_condition = models.CharField(max_length=50, choices=SOIL_CHOICES)
    weather = models.CharField(max_length=50, choices=WEATHER_CHOICES)
    temperature = models.FloatField(help_text='Temperature in °C', default=25.0)
    humidity = models.FloatField(help_text='Humidity percentage', default=60.0)
    planting_date = models.DateField()
    farm_area = models.FloatField(help_text='Farm area in acres', default=1.0)
    pest_image = models.ImageField(
        upload_to='pest_images/',
        blank=True,
        null=True,
        help_text='Upload an image for pest detection'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'farm_data'
        ordering = ['-created_at']
        verbose_name = 'Farm Data'
        verbose_name_plural = 'Farm Data Records'

    def __str__(self):
        return f"{self.user.username} - {self.get_crop_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class Alert(models.Model):
    """In-app alerts and notifications for farmers."""

    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    related_prediction = models.ForeignKey(
        'prediction.Prediction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"
