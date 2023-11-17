from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='Username')
    email = models.EmailField(max_length=32, verbose_name='Email')
    phone = models.CharField(max_length=32, verbose_name='Phone')
    password = models.CharField(max_length=32, verbose_name='Password')