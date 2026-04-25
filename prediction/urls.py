"""URL routing for prediction app."""

from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('result/<int:pk>/', views.PredictionResultView.as_view(), name='result'),
]
