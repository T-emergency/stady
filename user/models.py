from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.
username_validator = UnicodeUsernameValidator()
class User(AbstractUser):
    class Meta:
        db_table ='user'
    
    bio = models.CharField(max_length = 150, blank=True)
    department = models.CharField(max_length = 50, blank=True)
    age = models.CharField(max_length = 10, blank=True)
    profile_image = models.ImageField(upload_to='media', height_field=None, width_field=None, default='default.jpeg', blank=True)
    kakao_id = models.CharField(max_length=100, blank=True)
    total_time = models.IntegerField(default = 0)
    # local = models.CharField(max_length = 150, null = True)


# 사용자 개인정보, 핸드폰, 노출되곡 싶지않은 정보 유저랑, 유저 프로필 모델
# 관리자 권한, 회원등급 별로