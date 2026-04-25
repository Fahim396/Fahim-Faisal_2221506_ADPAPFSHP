"""
Admin panel views: Dashboard, User Management, Prediction Logs, Reports.
All views restricted to admin role only.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from accounts.decorators import admin_required
from accounts.models import User
from farmer.models import FarmData, Alert
from prediction.models import Prediction, Report


@method_decorator([login_required, admin_required], name='dispatch')
class AdminDashboardView(View):
    """Admin dashboard with system-wide statistics."""

    template_name = 'admin_panel/dashboard.html'

    def get(self, request):
        # System-wide stats
        total_farmers = User.objects.filter(role='farmer').count()
        total_predictions = Prediction.objects.count()
        total_farm_data = FarmData.objects.count()
        total_alerts = Alert.objects.filter(is_read=False).count()

        # Risk distribution for chart data
        risk_qs = Prediction.objects.values('risk_level').annotate(
            count=Count('id')
        )
        risk_map = {item['risk_level']: item['count'] for item in risk_qs}
        
        risk_distribution = [
            {'risk_level': 'low', 'count': risk_map.get('low', 0)},
            {'risk_level': 'medium', 'count': risk_map.get('medium', 0)},
            {'risk_level': 'high', 'count': risk_map.get('high', 0)},
        ]

        # Crop distribution
        crop_distribution = FarmData.objects.values('crop_type').annotate(
            count=Count('id')
        ).order_by('-count')[:6]

        # Recent activity
        recent_predictions = Prediction.objects.select_related(
            'farm_data__user'
        ).order_by('-created_at')[:10]

        # New farmers this month
        month_ago = timezone.now() - timedelta(days=30)
        new_farmers = User.objects.filter(
            role='farmer', created_at__gte=month_ago
        ).count()

        # Average confidence score
        avg_confidence = Prediction.objects.aggregate(
            avg=Avg('confidence_score')
        )['avg'] or 0

        # High risk predictions count
        high_risk = Prediction.objects.filter(risk_level='high').count()

        context = {
            'total_farmers': total_farmers,
            'total_predictions': total_predictions,
            'total_farm_data': total_farm_data,
            'total_alerts': total_alerts,
            'risk_distribution': list(risk_distribution),
            'crop_distribution': list(crop_distribution),
            'recent_predictions': recent_predictions,
            'new_farmers': new_farmers,
            'avg_confidence': avg_confidence,
            'high_risk': high_risk,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, admin_required], name='dispatch')
class UserManagementView(View):
    """CRUD operations for farmer accounts."""

    template_name = 'admin_panel/users.html'

    def get(self, request):
        users = User.objects.filter(role='farmer').order_by('-created_at')
        context = {'users': users}
        return render(request, self.template_name, context)


@method_decorator([login_required, admin_required], name='dispatch')
class ToggleUserStatusView(View):
    """Activate/deactivate a user account."""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, role='farmer')
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} has been {status}.')
        return redirect('admin_panel:users')


@method_decorator([login_required, admin_required], name='dispatch')
class DeleteUserView(View):
    """Delete a farmer account."""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, role='farmer')
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted.')
        return redirect('admin_panel:users')


@method_decorator([login_required, admin_required], name='dispatch')
class PredictionLogsView(View):
    """View all prediction logs across the system."""

    template_name = 'admin_panel/prediction_logs.html'

    def get(self, request):
        predictions = Prediction.objects.select_related(
            'farm_data__user'
        ).order_by('-created_at')

        # Filters
        risk_filter = request.GET.get('risk', '')
        crop_filter = request.GET.get('crop', '')

        if risk_filter:
            predictions = predictions.filter(risk_level=risk_filter)
        if crop_filter:
            predictions = predictions.filter(farm_data__crop_type=crop_filter)

        context = {
            'predictions': predictions,
            'risk_filter': risk_filter,
            'crop_filter': crop_filter,
            'crop_choices': FarmData.CROP_CHOICES,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, admin_required], name='dispatch')
class ReportsView(View):
    """Reports and analytics page."""

    template_name = 'admin_panel/reports.html'

    def get(self, request):
        # Generate report data
        risk_stats_qs = Prediction.objects.values('risk_level').annotate(
            count=Count('id'),
            avg_confidence=Avg('confidence_score')
        )
        risk_stats_map = {item['risk_level']: item for item in risk_stats_qs}
        
        risk_stats = [
            {'risk_level': 'low', 'count': risk_stats_map.get('low', {}).get('count', 0), 'avg_confidence': risk_stats_map.get('low', {}).get('avg_confidence', 0.0)},
            {'risk_level': 'medium', 'count': risk_stats_map.get('medium', {}).get('count', 0), 'avg_confidence': risk_stats_map.get('medium', {}).get('avg_confidence', 0.0)},
            {'risk_level': 'high', 'count': risk_stats_map.get('high', {}).get('count', 0), 'avg_confidence': risk_stats_map.get('high', {}).get('avg_confidence', 0.0)},
        ]

        crop_stats = FarmData.objects.values('crop_type').annotate(
            count=Count('id')
        ).order_by('-count')

        weather_stats = FarmData.objects.values('weather').annotate(
            count=Count('id')
        ).order_by('-count')

        # Monthly prediction counts (last 6 months)
        monthly_data = []
        for i in range(5, -1, -1):
            month_start = timezone.now().replace(day=1) - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            count = Prediction.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()
            monthly_data.append({
                'month': month_start.strftime('%b %Y'),
                'count': count
            })

        saved_reports = Report.objects.all().order_by('-created_at')[:10]

        context = {
            'risk_stats': list(risk_stats),
            'crop_stats': list(crop_stats),
            'weather_stats': list(weather_stats),
            'monthly_data': monthly_data,
            'saved_reports': saved_reports,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, admin_required], name='dispatch')
class DataMonitoringView(View):
    """Data monitoring panel showing all farm data entries."""

    template_name = 'admin_panel/data_monitoring.html'

    def get(self, request):
        farm_data = FarmData.objects.select_related('user').order_by('-created_at')
        context = {'farm_data': farm_data}
        return render(request, self.template_name, context)
