
import django
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's25.settings')
django.setup()

from web import models
models.UserInfo.objects.create(username='Lydia', email='lydia@gmail.com', mobile_phone='+15879203182', password='testpassword')