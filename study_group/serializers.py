from rest_framework import serializers

from study_group.models import StudentPost, StudentPostComment, Study, Student, Tag


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user.username
        return user

    def get_post(self, obj):
        post = obj.post.id
        return post

    def get_user_id(self, obj):
        user_id = obj.user.id
        return user_id

    class Meta:
        model = Student
        fields = '__all__'


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = '__all__'
        # fields = ["id", "user", "title", "content", "is_online",
                #   "now_cnt", "headcount", "thumbnail_img", "tags"]
        read_only_fields = ['tags', 'like']
        
        

    user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()  # readonly fields
    now_cnt = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept=True).count()

    def create(self, validated_data):
        validated_data['tags'] = self.context['tags']

        instance = super().create(validated_data)
        return instance


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fileds = ['name', ]

# 다른 방법은 없는지 찾아보고 & 여쭤보기 # 이방법은 데이터 베이스를 많이 참조하지 않나라는 생각?


class StudyDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    is_student = serializers.SerializerMethodField()
    sended = serializers.SerializerMethodField()
    thumbnail_img = serializers.SerializerMethodField()
    now_cnt = serializers.SerializerMethodField()
    # tags = TagSerializer(read_only = True, many = True)
    tags = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_is_like(self, obj):
        flag = obj.like.filter(id=self.context.get('request').user.id).exists()
        return flag

    def get_is_author(self, obj):
        print(obj.user, self.context.get('request').user)
        flag = False
        if obj.user == self.context.get('request').user:
            flag = True
        return flag

    def get_is_student(self, obj):
        flag = obj.student_set.filter(user=self.context.get(
            'request').user, post=obj, is_accept=True).exists()
        return flag

    def get_sended(self, obj):
        flag = obj.student_set.filter(user=self.context.get(
            'request').user, post=obj, is_accept=None).exists()
        return flag

    def get_thumbnail_img(self, obj):
        return obj.thumbnail_img.url

    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept=True).count()

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    class Meta:
        model = Study
        fields = ['id', 'user', 'headcount', 'title', 'content', 'is_online', 'is_like', 'is_penalty', 'days','limit_type', 'limit_time', 'week_penalty','total_penalty','penalty',
                  'thumbnail_img', 'is_author', 'is_student', 'sended', 'now_cnt', 'tags']
        read_only_fields = ['tags', ]


class PrivateStudentPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_author(self,obj):
        return obj.author.username

    def get_like_count(self, obj):
        return obj.like.count()

    def get_comment_count(self, obj):
        return obj.studentpostcomment_set.count()

    class Meta:
        model = StudentPost
        fields = '__all__'
        read_only_fields = ['study', 'author']

class PrivateStudentPostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    def get_author(self,obj):
        return obj.author.username
    def get_author_id(self,obj):
        return obj.author.id
    def get_comments(self, obj):
        comments = obj.studentpostcomment_set.order_by('-create_dt')
        serializer = PrivateStudyPostCommentSerializer(comments, many = True)
        return serializer.data

    def get_is_like(self, obj):
        user = self.context.get('request').user
        flag = obj.like.filter(user_id = user.id, is_accept = True).exists()
        return flag
    
    def get_like(self, obj):
        return obj.like.count()

    class Meta:
        model = StudentPost
        fields = '__all__'
        read_only_fields = ['study', 'author']

class PrivateStudyDetailSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    def get_students(self, obj):
        # 외래키를 사용하지 않았을 경우 생각하여
        obj_list = Student.objects.filter(post_id = obj.id, is_accept = True)
        return StudentSerializer(obj_list, many= True).data

    class Meta:
        model = Study
        fields = "__all__"

class PrivateStudyAuthorDetailSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    propose_students = serializers.SerializerMethodField()

    def get_students(self, obj):
        # 외래키를 사용하지 않았을 경우 생각하여
        obj_list = Student.objects.filter(post_id = obj.id, is_accept = True)
        return StudentSerializer(obj_list, many= True).data
    
    def get_propose_students(self, obj):
        obj_list = Student.objects.filter(post_id = obj.id, is_accept = None)
        return StudentSerializer(obj_list, many= True).data


    class Meta:
        model = Study
        fields = "__all__"

class PrivateStudyPostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def get_author_id(self,obj):
        return obj.author.id

    class Meta:
        model  = StudentPostComment
        fields = "__all__"
        read_only_fields = ['post',]