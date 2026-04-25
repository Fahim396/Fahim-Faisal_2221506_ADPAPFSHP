"""
Forms for the farmer module: farm data entry.
"""

from django import forms
from .models import FarmData


class FarmDataForm(forms.ModelForm):
    """Form for farmers to enter farm data for pest prediction."""

    class Meta:
        model = FarmData
        fields = [
            'crop_type', 'soil_condition', 'weather',
            'temperature', 'humidity', 'planting_date',
            'farm_area', 'pest_image', 'notes'
        ]
        widgets = {
            'crop_type': forms.Select(attrs={
                'class': 'form-input',
                'id': 'farm-crop-type'
            }),
            'soil_condition': forms.Select(attrs={
                'class': 'form-input',
                'id': 'farm-soil'
            }),
            'weather': forms.Select(attrs={
                'class': 'form-input',
                'id': 'farm-weather'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Temperature (°C)',
                'id': 'farm-temp',
                'step': '0.1'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Humidity (%)',
                'id': 'farm-humidity',
                'step': '0.1'
            }),
            'planting_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'id': 'farm-planting-date'
            }),
            'farm_area': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Area (acres)',
                'id': 'farm-area',
                'step': '0.1'
            }),
            'pest_image': forms.FileInput(attrs={
                'class': 'form-input file-input',
                'id': 'farm-pest-image',
                'accept': 'image/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional notes...',
                'id': 'farm-notes',
                'rows': 3
            }),
        }
