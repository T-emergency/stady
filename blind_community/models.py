from django.db import models
from user.models import User



class Post(models.Model):
    class Meta:
        db_table = 'blind_community_post'
    
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='user_post')
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to='post' , blank = True)
    category = models.CharField(max_length = 15, null = True)



class PostComment(models.Model):
    class Meta:
        db_table = 'blind_community_comment'

    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True) #하나의 post를 볼 수 있게 pk
    content = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
    # 타이틀 content로 _ 다지우기


class RandomName(models.Model):
    class Meta:
        db_table = 'random_name2'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_random')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null = True, related_name='random_post')
    random_name = models.CharField(max_length=100, null = False)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null = True, related_name='post_like')
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, null=True, related_name='comment_like')
    like = models.BooleanField(default=False)
