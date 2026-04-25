"""
Mock AI Prediction Service.
=============================================================================
This module simulates an AI pest prediction engine using rule-based logic.
It is designed as a drop-in replacement interface — when a real ML model is
ready, simply replace the `predict()` method internals.

Architecture:
    FarmData → PestPredictionService.predict() → Prediction record

The service uses environmental factors (weather, humidity, temperature, soil,
crop type) to compute a weighted risk score, then maps it to Low/Medium/High.
=============================================================================
"""

import random
import hashlib
from datetime import date
from .models import Prediction


class PestPredictionService:
    """
    Mock AI service for pest attack prediction.

    Replace the internals of `predict()` with a real ML model call
    (e.g., TensorFlow, PyTorch, or external API) for production use.
    """

    # ── Risk factor weights ──────────────────────────────────────────
    WEATHER_RISK = {
        'sunny': 0.2,
        'cloudy': 0.3,
        'rainy': 0.7,
        'humid': 0.8,
        'dry': 0.3,
        'windy': 0.4,
        'stormy': 0.6,
    }

    SOIL_RISK = {
        'clay': 0.5,
        'sandy': 0.3,
        'loamy': 0.4,
        'silt': 0.5,
        'peat': 0.6,
        'chalk': 0.3,
        'other': 0.4,
    }

    CROP_VULNERABILITY = {
        'rice': 0.7,
        'wheat': 0.4,
        'corn': 0.5,
        'cotton': 0.8,
        'sugarcane': 0.6,
        'potato': 0.5,
        'tomato': 0.7,
        'soybean': 0.4,
        'vegetables': 0.6,
        'fruits': 0.5,
        'other': 0.5,
    }

    # ── Common pests per crop ────────────────────────────────────────
    PEST_DATABASE = {
        'rice': ['Brown Planthopper', 'Rice Stem Borer', 'Rice Blast Fungus', 'Leaf Folder'],
        'wheat': ['Aphids', 'Hessian Fly', 'Wheat Rust', 'Armyworm'],
        'corn': ['Fall Armyworm', 'Corn Borer', 'Corn Earworm', 'Rootworm'],
        'cotton': ['Bollworm', 'Whitefly', 'Pink Bollworm', 'Jassids'],
        'sugarcane': ['Sugarcane Borer', 'Pyrilla', 'Termites', 'Scale Insect'],
        'potato': ['Colorado Beetle', 'Potato Tuber Moth', 'Aphids', 'Late Blight'],
        'tomato': ['Tomato Hornworm', 'Whitefly', 'Spider Mites', 'Leaf Miner'],
        'soybean': ['Soybean Aphid', 'Bean Leaf Beetle', 'Stink Bug', 'Pod Borer'],
        'vegetables': ['Aphids', 'Caterpillars', 'Whitefly', 'Thrips'],
        'fruits': ['Fruit Fly', 'Codling Moth', 'Scale Insect', 'Mealybug'],
        'other': ['General Pest', 'Aphids', 'Caterpillars', 'Mites'],
    }

    # ── Recommendations ─────────────────────────────────────────────
    RECOMMENDATIONS = {
        'low': [
            'Continue regular monitoring of your crops.',
            'Maintain current pest prevention measures.',
            'Schedule next inspection in 2 weeks.',
            'Ensure proper drainage to prevent moisture buildup.',
            'Consider applying preventive organic treatments.',
        ],
        'medium': [
            'Increase monitoring frequency to twice per week.',
            'Apply organic pest control measures as a precaution.',
            'Inspect leaf undersides and stems for early signs.',
            'Consider introducing beneficial insects (ladybugs, lacewings).',
            'Prepare targeted pesticide application if situation worsens.',
            'Consult with a local agricultural extension officer.',
        ],
        'high': [
            'IMMEDIATE ACTION REQUIRED: Apply appropriate pesticide treatment.',
            'Isolate affected areas to prevent pest spread.',
            'Contact local agricultural authority for guidance.',
            'Consider early harvest of unaffected portions to minimize loss.',
            'Document damage for insurance and record-keeping purposes.',
            'Implement integrated pest management (IPM) strategies.',
            'Schedule follow-up assessment within 3 days.',
        ],
    }

    def predict(self, farm_data):
        """
        Generate a pest attack prediction based on farm data.

        Args:
            farm_data: FarmData model instance

        Returns:
            Prediction model instance (saved to database)

        Note:
            Replace this method's internals with actual ML model inference
            for production deployment.
        """
        # ── Calculate composite risk score ───────────────────────────
        weather_score = self.WEATHER_RISK.get(farm_data.weather, 0.5)
        soil_score = self.SOIL_RISK.get(farm_data.soil_condition, 0.4)
        crop_score = self.CROP_VULNERABILITY.get(farm_data.crop_type, 0.5)

        # Temperature risk: higher risk at extreme temperatures
        temp = farm_data.temperature
        if temp > 35 or temp < 10:
            temp_score = 0.8
        elif temp > 30 or temp < 15:
            temp_score = 0.6
        else:
            temp_score = 0.3

        # Humidity risk: higher humidity = higher pest risk
        humidity = farm_data.humidity
        if humidity > 80:
            humidity_score = 0.9
        elif humidity > 60:
            humidity_score = 0.6
        elif humidity > 40:
            humidity_score = 0.4
        else:
            humidity_score = 0.2

        # Planting age factor: young and mature crops are more vulnerable
        days_since_planting = (date.today() - farm_data.planting_date).days
        if days_since_planting < 30:
            age_score = 0.7  # Seedling stage — vulnerable
        elif days_since_planting < 90:
            age_score = 0.4  # Vegetative — moderate
        else:
            age_score = 0.6  # Mature — somewhat vulnerable

        # ── Weighted composite score ─────────────────────────────────
        composite = (
            weather_score * 0.25 +
            soil_score * 0.10 +
            crop_score * 0.20 +
            temp_score * 0.15 +
            humidity_score * 0.20 +
            age_score * 0.10
        )

        # Add deterministic pseudo-randomness based on farm data ID
        seed_str = f"{farm_data.pk}-{farm_data.crop_type}-{farm_data.weather}"
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
        noise = (seed_hash % 100) / 1000 - 0.05  # Range: -0.05 to +0.05
        composite = max(0.0, min(1.0, composite + noise))

        # ── Determine risk level ─────────────────────────────────────
        if composite >= 0.65:
            risk_level = 'high'
        elif composite >= 0.40:
            risk_level = 'medium'
        else:
            risk_level = 'low'

        # ── Select predicted pest ────────────────────────────────────
        pests = self.PEST_DATABASE.get(farm_data.crop_type, self.PEST_DATABASE['other'])
        random.seed(seed_hash)
        predicted_pest = random.choice(pests)

        # ── Build recommendation ─────────────────────────────────────
        recs = self.RECOMMENDATIONS[risk_level]
        random.seed(seed_hash + 1)
        selected_recs = random.sample(recs, min(3, len(recs)))
        recommendation = '\n'.join(f"• {r}" for r in selected_recs)

        # ── Build detail breakdown ───────────────────────────────────
        details = {
            'factors': {
                'weather': {'value': farm_data.weather, 'score': round(weather_score, 2)},
                'soil': {'value': farm_data.soil_condition, 'score': round(soil_score, 2)},
                'crop': {'value': farm_data.crop_type, 'score': round(crop_score, 2)},
                'temperature': {'value': farm_data.temperature, 'score': round(temp_score, 2)},
                'humidity': {'value': farm_data.humidity, 'score': round(humidity_score, 2)},
                'crop_age_days': {'value': days_since_planting, 'score': round(age_score, 2)},
            },
            'composite_score': round(composite, 4),
            'model_version': 'mock-v1.0',
            'note': 'This is a simulated prediction. Replace with real ML model for production.',
        }

        # ── Save and return prediction ───────────────────────────────
        prediction = Prediction.objects.create(
            farm_data=farm_data,
            risk_level=risk_level,
            confidence_score=round(composite, 4),
            predicted_pest=predicted_pest,
            recommendation=recommendation,
            details=details,
        )

        return prediction
