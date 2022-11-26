from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.
# username_validator = UnicodeUsernameValidator()
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# class User(AbstractUser):
#     class Meta:
#         db_table ='user'
    
#     bio = models.CharField(max_length = 150, blank=True)
#     department = models.CharField(max_length = 50, blank=True)
#     age = models.CharField(max_length = 10, blank=True)
#     profile_image = models.ImageField(upload_to='media', height_field=None, width_field=None, default='default.jpeg', blank=True)
#     kakao_id = models.CharField(max_length=100, blank=True)
#     total_time = models.IntegerField(default = 0)
    # local = models.CharField(max_length = 150, null = True)

#TODO 관심 분야, 카카오, 총 시간, 지역 저장하기
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email = email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name = 'username',
        max_length = 128,
        unique = True,
    )
    total_time = models.IntegerField(default = 0)
    department = models.ForeignKey('study_group.Category', on_delete = models.CASCADE, null = True, blank = True)
    profile_image = models.ImageField(upload_to='media', height_field=None, width_field=None, default='default.jpeg', blank=True)
    kakao_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin