"""URL routing for admin panel app."""

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),
    path('users/', views.UserManagementView.as_view(), name='users'),
    path('users/<int:pk>/toggle/', views.ToggleUserStatusView.as_view(), name='toggle_user'),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
    path('predictions/', views.PredictionLogsView.as_view(), name='prediction_logs'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('monitoring/', views.DataMonitoringView.as_view(), name='data_monitoring'),
]
