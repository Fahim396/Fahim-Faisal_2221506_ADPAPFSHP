"""URL routing for accounts app."""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('redirect/', views.RoleRedirectView.as_view(), name='redirect'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
