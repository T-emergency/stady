from django.db import models
from user.models import User
# Create your models here.

class StudyLog(models.Model):
    # 공부시간 로그
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add = True)
    start_time = models.DateTimeField(auto_now_add = True)
    end_time = models.DateTimeField(blank = True, null= True)
    memo = models.TextField(blank = True)


class InStudy(models.Model):
    # 참여 로그
    log = models.ForeignKey(StudyLog, on_delete = models.CASCADE)
    in_time = models.DateTimeField(auto_now_add = True)
    out_time = models.DateTimeField(blank = True, null = True)

class OutStudy(models.Model):
    # 불참여 로그
    log = models.ForeignKey(StudyLog, on_delete = models.CASCADE)
    out_time = models.DateTimeField(auto_now_add = True)
    in_time = models.DateTimeField(null = True)
