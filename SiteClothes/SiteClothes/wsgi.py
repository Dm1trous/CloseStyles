import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiteClothes.settings') # Убедитесь, что 'SiteClothes' - это имя вашей папки с проектом
application = get_wsgi_application()