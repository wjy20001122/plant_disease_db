"""
WSGI config for plant_disease_db project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_disease_db.settings')

application = get_wsgi_application()

