"""WSGI config for smart_harvest project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_harvest.settings')
application = get_wsgi_application()
