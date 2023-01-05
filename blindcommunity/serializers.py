from rest_framework import serializers
from .models import Post, PostComment, RandomName

# 검색
class PostSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields='__all__'


# 인기글
class TopPostListSerializer(serializers.ModelSerializer):
    user =serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()
# 카운트
# 이런식으로 사용하면 되는지 발표 피드백에서 시리얼라이저를 사용할때 하나의 시리얼라이저로 여러가지 방식으로 사용할 수 있다고 했다.
# 방식을 다르게 하는것도 괜찮다고 하셔서 어떤식으로 사용 할 수 있는지
# 메소드 필드에 의존하지말라
# 장고 벨리데이터가 있다
# 모델에서 정의를 벨리데이터로 넘어간다. 조건을 검증한다.
# 검증내용을 프론트에서 1차 거른다 비밀번호 조거이라든가 잘못입력한거 js로 사용자 경험이 좋아진다. 실제로는 데이터관리 모델 백엔드
# 시리얼라이저가 가지고있다 기본적으로 벨리데이터 /  커스터마이즈 해서 사용
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
    def get_likes_count(self, obj): #카운트 어그리게이트 어노테이트 사용가능 모델에서 조작가능 / 모델에서 카운트를 기록
        return obj.likes.count()
    def get_created_date(self,obj):
        return str(obj.created_date)[:19] # 프론트에서 조작해도 괜찮다. 처음엔 왜 메소드필드 썻는지 모르겠다 하심
    class Meta:
        model = Post
        fields=('title','content','user','likes_count','comments_count','hits','category','id','created_date')


# 게시글 리스트
class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count =serializers.SerializerMethodField()
    created_date= serializers.SerializerMethodField()
    img=serializers.ImageField(use_url=True)

    def get_comments_count(self,obj):
        return obj.postcomment_set.count()
    def get_user(self, obj):
        post_id = obj.id
        user_id = obj.user_id
        category = Post.objects.filter(category = '익명게시판')
        if category:
            randomname = RandomName.objects.get(user_id=user_id, post_id=post_id)
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
    content = serializers.CharField(min_length=1, max_length=200) # 기왕할거면 모델에서 하는게 좋다.
    created_date= serializers.SerializerMethodField()

    
    def get_user_id(self, obj):
        return obj.user.id
    def get_user(self, obj):
        user=obj.user_id
        post=obj.post_id
        random_name=RandomName.objects.get(post_id=post, user_id=user)
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
class PostCreateSerializer(serializers.ModelSerializer):
    title=serializers.CharField(min_length=1, max_length=40)
    content=serializers.CharField(min_length=1, max_length=200)
    category=serializers.CharField(min_length=1, required=False)


    class Meta:
        model = Post
        fields = ("title","content","img","category")

        
class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')


class CommentDetailSerializer(serializers.ModelSerializer):
    content=serializers.CharField(min_length=5, max_length=200)

    class Meta:
        model = PostComment
        fields=("content",)
