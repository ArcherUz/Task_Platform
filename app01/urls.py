from django.urls import path, include
from app01 import views

urlpatterns = [
    path('send/sms/', views.send_sms_view),
    path('register/', views.register_view),
]
