from django.db import models
from user.models import User


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.tag_name}'


class Study(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail_img = models.ImageField(upload_to='media', height_field=None, default='default.jpeg', blank=True)
    on_off_line = models.BooleanField(default=False) # None 0 1 로 구분이 안된다면 CharField로 구분 # TODO is_on_line으로 변수명 변경
    headcount = models.IntegerField()  # IntegerChoices? 선택인원 최소 2~10 지정할 수 있으면 지정하기
    like = models.ManyToManyField(User, blank=True, related_name='liker')
    tags = models.ManyToManyField(Tag, related_name='tags', null=True, blank=True) # 참여자와 연동되는 이유는 여러 유저를 참조하는 것은 맞으나 is_accept를 사용하기 위해서
    submit = models.ManyToManyField("Student", blank=True, related_name='submiter') # category = #TODO 경민 - 조사 후 카테고리, 나눈 뒤 모델 생성

    def __str__(self):
        return f'{self.user} / {self.title}'

# Create your models here.


class Student(models.Model): # 참여자 모델
    class Meta:
        db_table = 'student'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Study, on_delete=models.CASCADE)
    join_dt = models.DateField(auto_now_add=True)
    is_accept = models.BooleanField(default=None, null=True)


class Bookmark(models.Model):
    post = models.ForeignKey(Study, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    high_class = models.CharField(max_length = 64)
    sub_class = models.CharField(max_length = 128)

    def __str__(self):
        return self.sub_class

class Tag(models.Model):
    tag_name = models.CharField(max_length = 128)