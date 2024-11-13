import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ASKME_BODNYA.settings')

application = get_wsgi_application()
