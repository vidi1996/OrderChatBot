"""
WSGI config for Orderproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

# add your project directory to the sys.path
project_home = u'/home/vidithavp/Orderproject'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Orderproject.settings')

application = get_wsgi_application()
