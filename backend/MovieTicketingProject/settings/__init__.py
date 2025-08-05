# MovieTicketingProject/settings/__init__.py

import os

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'MovieTicketingProject.settings.production':
    from .production import *
else:
    from .development import *