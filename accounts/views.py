"""
Authentication views: Register, Login, Logout, Role-based redirect.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator

from .forms import RegistrationForm, LoginForm, ProfileForm


class RegisterView(View):
    """Handle user registration with role selection."""

    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:redirect')
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Account created successfully.')
            return redirect('accounts:redirect')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Handle user login."""

    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:redirect')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('accounts:redirect')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Handle user logout."""

    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class RoleRedirectView(View):
    """Redirect user to their role-specific dashboard."""

    def get(self, request):
        if request.user.is_admin_user:
            return redirect('admin_panel:dashboard')
        return redirect('farmer:dashboard')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """User profile view and edit."""

    template_name = 'accounts/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})
