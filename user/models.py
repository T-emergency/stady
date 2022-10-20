from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table ='user'
    
    bio = models.CharField(max_length = 150, blank=True)
    department = models.CharField(max_length = 50, blank=True)
    age = models.CharField(max_length = 10, blank=True)
    nickname = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(upload_to='media', height_field=None, width_field=None, default='default.jpeg', blank=True)
    kakao_id = models.CharField(max_length=100, blank=True)
    # local = models.CharField(max_length = 150, null = True)


