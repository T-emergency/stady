from django.db import models
from user.models import User
# Create your models here.

class StudyLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add = True)
    start_time = models.DateTimeField(auto_now_add = True)
    end_time = models.DateTimeField(blank = True, null= True)


class InStudy(models.Model):
    log = models.ForeignKey(StudyLog, on_delete = models.CASCADE)
    in_time = models.DateTimeField(auto_now_add = True)
    out_time = models.DateTimeField(blank = True, null = True)

class OutStudy(models.Model):
    log = models.ForeignKey(StudyLog, on_delete = models.CASCADE)
    out_time = models.DateTimeField(auto_now_add = True)