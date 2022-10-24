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


# class 붕어틀:
#     앙금 =
#     반죽 =

# 붕어빵 1 = 뿡어틀()

# 붕어빵1.앙금 = 슈크림
# 붕어빵1.반죽 = 밀가루

# 붕어빵 2 = 뿡어틀()

# 붕어빵2.앙금 = 팥
# 붕어빵2.반죽 = 밀가루


# 붕어빵리스트 = [붕어빵1, 붕어빵2]

# 붕어빵가져오는변수 = 붕어틀.objects.filter(반죽 = 밀가루)

# def 붕어빵 해체함수(붕어빵리스트):
#     for i in 내맘변수:
#         print(i,'')
#     Print('쩝떱')

# 붕어빵 해체함수(내맘변수 = 붕어빵리스트)