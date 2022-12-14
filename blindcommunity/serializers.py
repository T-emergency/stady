from rest_framework import serializers
from .models import Post, PostComment, RandomName

# 검색
class PostSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields='__all__'


# 인기글에서 익명글은 익명name으로 보여야한다.
class TopPostListSerializer(serializers.ModelSerializer):
    user =serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()


    def get_user(self, obj):
        if obj.category=='익명게시판':
            post=obj.id
            user=obj.user_id
            random_name=RandomName.objects.get(user_id=user, post_id=post)
            return random_name.name
        else:
            return obj.user.username
    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:19]
    class Meta:
        model = Post
        fields=('title','content','user','likes_count','comments_count','hits','category','id','created_date')


# 게시글 리스트
class PostListSerializer(serializers.ModelSerializer): # get 게시글 리스트 불러오기
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()
    img=serializers.ImageField(use_url=True)

    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_user(self, obj):
        post = obj.id
        user = obj.user_id
        category = Post.objects.filter(category = '익명게시판')
        if category:
            randomname = RandomName.objects.get(user_id=user,post_id=post )
            return randomname.name
        return obj.user.username 
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:19]
    def get_user_id(self, obj):
        return obj.user.id

    def get_created_date(self,obj):
        return str(obj.created_date)[:10]


    class Meta:
        model = Post
        fields = ("title","content","likes_count","user","comments_count","category","hits","id","created_date","img","user_id","likes")
        read_only_fields=('likes_count',)


# 익명게시판 리스트, 익명게시글 디테일
class BlindPostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user(self, obj):
        post=obj.id
        user=obj.user_id
        random_name=RandomName.objects.get(user_id=user, post_id=post)
        return random_name.name
    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:19]
    def get_user_id(self, obj):
        return obj.user.id
        
    class Meta:
        model = Post
        fields=('title','content','user','likes_count','comments_count','hits','category','id','created_date','likes','user_id','img')


class BlindCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    content = serializers.CharField(min_length=1, max_length=200)
    created_date= serializers.SerializerMethodField()

    
    def get_user_id(self, obj):
        return obj.user.id
    def get_user(self, obj):
        user=obj.user_id
        post=obj.post_id
        random_name=RandomName.objects.get(post_id=post, user_id=user) # 하나밖에 없음
        return random_name.name
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:19]
    

    class Meta:
        model = PostComment
        fields=("content","likes_count","user","id","user_id","likes","created_date")

#게시글 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    content = serializers.CharField(max_length=200)
    created_date= serializers.SerializerMethodField()

    
    def get_user(self, obj):
        return obj.user.username
    def get_user_id(self, obj):
        return obj.user.id
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:19]
    
    class Meta:
        model = PostComment
        fields=("content","likes_count","user","id","user_id","created_date","likes")

# 게시글 생성
class PostCreateSerializer(serializers.ModelSerializer): # 게시글 생성
    title=serializers.CharField(min_length=1, max_length=40)
    content=serializers.CharField(min_length=1, max_length=200)
    category=serializers.CharField(min_length=1, required=False)


    class Meta:
        model = Post
        fields = ("title","content","img","category")

        
class PostDetailSerializer(serializers.ModelSerializer): # 게시글 디테일

    class Meta:
        model = Post
        fields = ('__all__')


class CommentDetailSerializer(serializers.ModelSerializer):
    content=serializers.CharField(min_length=5, max_length=200)

    class Meta:
        model = PostComment
        fields=("content",)
