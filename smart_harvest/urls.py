"""
Root URL configuration for smart_harvest project.
Routes are organized per app for clean separation of concerns.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),

    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # App routes
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('farmer/', include('farmer.urls', namespace='farmer')),
    path('panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('prediction/', include('prediction.urls', namespace='prediction')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
