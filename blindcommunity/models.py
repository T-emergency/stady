from django.db import models
from user.models import User



class Post(models.Model):
    class Meta:
        db_table = 'community_post'
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='post' , blank = True)
    likes=models.ManyToManyField(User,related_name='post_like',blank=True)
    hits =models.IntegerField(default=0)
    category=models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f'{self.user} / {self.content} / {self.title} / {self.category} / {self.hits}/'


class PostComment(models.Model):
    class Meta:
        db_table = 'community_comment'

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE) #하나의 post를 볼 수 있게 pk
    content = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_like',blank=True)
    

    def __str__(self):
        return f'{str(self.user)} / {str(self.content)}'


class RandomName(models.Model):
    class Meta:
        db_table='random_name'
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='random_user', blank=True, null=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='random_post', blank=True, null=True)
    name=models.CharField(max_length=30)

    def __str__(self):
        return f'{str(self.name)} / {str(self.user)} / {str(self.post)} '


