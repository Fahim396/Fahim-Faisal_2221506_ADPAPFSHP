"""
Farmer module views: Dashboard, data entry, history, alerts.
All views are class-based and role-protected.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.db.models import Count

from accounts.decorators import farmer_required
from .models import FarmData, Alert
from .forms import FarmDataForm
from prediction.models import Prediction
from prediction.services import PestPredictionService


@method_decorator([login_required, farmer_required], name='dispatch')
class FarmerDashboardView(View):
    """Farmer dashboard with overview stats."""

    template_name = 'farmer/dashboard.html'

    def get(self, request):
        farm_data_count = FarmData.objects.filter(user=request.user).count()
        prediction_count = Prediction.objects.filter(farm_data__user=request.user).count()
        unread_alerts = Alert.objects.filter(user=request.user, is_read=False).count()

        recent_predictions = Prediction.objects.filter(
            farm_data__user=request.user
        ).select_related('farm_data').order_by('-created_at')[:5]

        recent_alerts = Alert.objects.filter(
            user=request.user, is_read=False
        ).order_by('-created_at')[:5]

        # Stats for dashboard cards
        high_risk_count = Prediction.objects.filter(
            farm_data__user=request.user, risk_level='high'
        ).count()

        context = {
            'farm_data_count': farm_data_count,
            'prediction_count': prediction_count,
            'unread_alerts': unread_alerts,
            'high_risk_count': high_risk_count,
            'recent_predictions': recent_predictions,
            'recent_alerts': recent_alerts,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, farmer_required], name='dispatch')
class DataEntryView(View):
    """Farm data entry form for pest prediction."""

    template_name = 'farmer/data_entry.html'

    def get(self, request):
        form = FarmDataForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FarmDataForm(request.POST, request.FILES)
        if form.is_valid():
            farm_data = form.save(commit=False)
            farm_data.user = request.user
            farm_data.save()

            # Run mock AI prediction
            service = PestPredictionService()
            prediction = service.predict(farm_data)

            # Create alert if risk is medium or high
            if prediction.risk_level in ['medium', 'high']:
                Alert.objects.create(
                    user=request.user,
                    title=f'Pest Risk Alert: {prediction.get_risk_level_display()}',
                    message=f'Your {farm_data.get_crop_type_display()} farm has a '
                            f'{prediction.get_risk_level_display()} pest risk '
                            f'(Confidence: {prediction.confidence_score:.0%}). '
                            f'Please review the recommendations.',
                    severity='critical' if prediction.risk_level == 'high' else 'warning',
                    related_prediction=prediction,
                )

            messages.success(request, 'Farm data submitted! Prediction generated.')
            return redirect('prediction:result', pk=prediction.pk)
        return render(request, self.template_name, {'form': form})


@method_decorator([login_required, farmer_required], name='dispatch')
class HistoryView(View):
    """View past predictions and farm data entries."""

    template_name = 'farmer/history.html'

    def get(self, request):
        predictions = Prediction.objects.filter(
            farm_data__user=request.user
        ).select_related('farm_data').order_by('-created_at')

        context = {'predictions': predictions}
        return render(request, self.template_name, context)


@method_decorator([login_required, farmer_required], name='dispatch')
class AlertListView(View):
    """View and manage alerts."""

    template_name = 'farmer/alerts.html'

    def get(self, request):
        alerts = Alert.objects.filter(user=request.user).order_by('-created_at')
        context = {'alerts': alerts}
        return render(request, self.template_name, context)


@method_decorator([login_required, farmer_required], name='dispatch')
class MarkAlertReadView(View):
    """Mark an alert as read."""

    def post(self, request, pk):
        alert = get_object_or_404(Alert, pk=pk, user=request.user)
        alert.is_read = True
        alert.save()
        return redirect('farmer:alerts')
