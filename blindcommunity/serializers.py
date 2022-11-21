from rest_framework import serializers
from .models import Post, PostComment, RandomName

# 검색
class PostSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields='__all__'

# 인기글에서 익명글은 익명name으로 보여야지
class TopPostListSerializer(serializers.ModelSerializer):
    user =serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()


    def get_user(self, obj):
        if obj.category=='blind':
            a=obj.id
            b=obj.user_id
            c=RandomName.objects.get(user_id=b, post_id=a)
            return c.name
        else:
            return obj.user.username
    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:10]
    class Meta:
        model = Post
        fields=('title','content','user','likes_count','comments_count','hits','category','id','created_date')


# 게시글 리스트
class PostListSerializer(serializers.ModelSerializer): # get 게시글 리스트 불러오기
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()


    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_user(self, obj):
        return obj.user.username 
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:10]

    class Meta:
        model = Post
        fields = ("title","content","likes_count","user","comments_count","category","hits","id","created_date")
        read_only_fields=('likes_count',) 

# 익명게시판 리스트, 익명게시글 디테일
class BlindPostListSerializer(serializers.ModelSerializer):
    user =serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()


    def get_user(self, obj):
        a=obj.id
        b=obj.user_id
        c=RandomName.objects.get(user_id=b, post_id=a)
        return c.name
    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:10]
        
    class Meta:
        model = Post
        fields=('title','content','user','likes_count','comments_count','hits','category','id','created_date')



class BlindCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        a=obj.user_id
        b=obj.post_id
        c=RandomName.objects.get(post_id=b, user_id=a) # 하나밖에 없음
        return c.name
    

    class Meta:
        model = PostComment
        fields='__all__'

#게시글 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username 
    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = PostComment
        fields=("content","likes_count","user")



class PostCreateSerializer(serializers.ModelSerializer): # 게시글 생성

    class Meta:
        model = Post
        fields = ("title","content","img","category")
        read_only_fields=('img',)

class PostDetailSerializer(serializers.ModelSerializer): # 게시글 디테일

    class Meta:
        model = Post
        fields = ('__all__')



class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields=("content",)