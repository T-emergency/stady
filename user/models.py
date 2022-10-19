from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table ='user'
    
    bio = models.CharField(max_length = 150, blank=True)
    department = models.CharField(max_length = 50, blank=True)
    age = models.CharField(max_length = 10, blank=True)
    profile_image = models.ImageField(upload_to='media', height_field=None, width_field=None, default='default.jpeg')

    # local = models.CharField(max_length = 150, null = True)



class Follow(models.Model):
    class Meta:
        db_table ='follow'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follow = models.ForeignKey(User, on_delete =models.CASCADE, related_name ='follow')