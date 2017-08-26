"""
WSGI config for lap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.extend(
    [
        '/srv/django-projects/ihc-image-analysis/lap',
        '/srv/django-projects/ihc-image-analysis'
    ]
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lap.settings")

application = get_wsgi_application()
