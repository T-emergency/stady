from django.db import models
from user.models import User


# Create your models here.


class Post(models.Model):
    class Meta:
        db_table = 'community_post'

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post_title = models.CharField(max_length=50)
    post_content = models.CharField(max_length=200)
    create_date = models.DateTimeField(blank = True)
    image = models.ImageField(upload_to='post')



class PostComment(models.Model):
    class Meta:
        db_table = 'community_comment'
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_content = models.CharField(max_length=100)
    create_date = models.DateTimeField(blank = True)
