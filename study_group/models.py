from django.db import models
from user.models import User


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.tag_name}'


class Study(models.Model):
    STUDY_TYPE = (
        ('TT', '총 공부 시간'), # total time
        ('CT', '출석 체크 시간'), # check time
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail_img = models.ImageField(
        upload_to='media', height_field=None, default='default.jpeg', blank=True)
    # None 0 1 로 구분이 안된다면 CharField로 구분
    is_online = models.BooleanField(default=True)
    headcount = models.IntegerField()  # IntegerChoices? 선택인원 최소 2~10 지정할 수 있으면 지정하기
    like = models.ManyToManyField(User, related_name='liker')
    # 참여자와 연동되는 이유는 여러 유저를 참조하는 것은 맞으나 is_accept를 사용하기 위해서
    submit = models.ManyToManyField(
        "Student", related_name='submiter', blank=True)
    tags = models.ManyToManyField(
        "Tag", related_name='tag_studies', blank=True)
    # 벌금 스터디
    total_money = models.IntegerField(default = 0)
    week_money = models.IntegerField(default = 0) # 주가 끝나는 날 초기화

    is_penalty = models.BooleanField(default = False)
    days = models.CharField(max_length = 7, blank = True)
    limit_type = models.CharField(max_length = 5, choices=STUDY_TYPE, blank = True)
    limit_time = models.SmallIntegerField(null = True,blank = True)

    def __str__(self):
        return f'{self.user} / {self.title}'


class Student(models.Model):  # 참여자 모델
    class Meta:
        db_table = 'student'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Study, on_delete=models.CASCADE)
    join_dt = models.DateField(auto_now_add=True)
    is_accept = models.BooleanField(default=None, null=True)
    total_penalty = models.IntegerField(default = 0)
    week_penalty = models.IntegerField(default = 0) # 주가 끝나는 날 초기화


class StudentPost(models.Model):
    class Meta:
        db_table = "student_post"
    study = models.ForeignKey(Study, on_delete= models.CASCADE)
    author = models.ForeignKey(Student, on_delete= models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)



class Bookmark(models.Model):
    post = models.ForeignKey(Study, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    high_class = models.CharField(max_length=64)
    sub_class = models.CharField(max_length=128)

    def __str__(self):
        return self.sub_class


class UserTagLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
