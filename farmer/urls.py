"""URL routing for farmer app."""

from django.urls import path
from . import views

app_name = 'farmer'

urlpatterns = [
    path('dashboard/', views.FarmerDashboardView.as_view(), name='dashboard'),
    path('data-entry/', views.DataEntryView.as_view(), name='data_entry'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('alerts/', views.AlertListView.as_view(), name='alerts'),
    path('alerts/<int:pk>/read/', views.MarkAlertReadView.as_view(), name='mark_alert_read'),
]
