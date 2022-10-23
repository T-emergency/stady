from django.db import models
from user.models import User


# Create your models here.


class Post(models.Model):
    class Meta:
        db_table = 'community_post'
    
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    create_date = models.DateTimeField(blank = True)
    image = models.ImageField(upload_to='post' , blank = True)



class PostComment(models.Model):
    class Meta:
        db_table = 'community_comment'

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE) #하나의 post를 볼 수 있게 pk
    content = models.CharField(max_length=100)
    create_date = models.DateTimeField(blank = True)

    # 타이틀 content로 _ 다지우기
