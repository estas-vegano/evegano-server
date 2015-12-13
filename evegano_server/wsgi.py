"""
WSGI config for evegano_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evegano_server.settings")

application = get_wsgi_application()
