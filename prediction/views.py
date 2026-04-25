"""
Prediction views: result display.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from .models import Prediction


@method_decorator(login_required, name='dispatch')
class PredictionResultView(View):
    """Display prediction result for a specific farm data entry."""

    template_name = 'farmer/prediction_result.html'

    def get(self, request, pk):
        prediction = get_object_or_404(
            Prediction.objects.select_related('farm_data'),
            pk=pk,
            farm_data__user=request.user
        )
        context = {'prediction': prediction}
        return render(request, self.template_name, context)
