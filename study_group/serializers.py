from rest_framework import serializers

from study_group.models import StudentPost, Study, Student, Tag


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
        fields = ["id", "user", "title", "content", "is_online",
                  "now_cnt", "headcount", "thumbnail_img", "tags"]

    user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()  # readonly fields
    now_cnt = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept=True).count() + 1

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
        return obj.student_set.filter(is_accept=True).count() + 1

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    class Meta:
        model = Study
        fields = ['id', 'user', 'headcount', 'title', 'content', 'is_online', 'is_like',
                  'thumbnail_img', 'is_author', 'is_student', 'sended', 'now_cnt', 'tags']
        read_only_fields = ['tags', ]


class PrivateStudentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPost
        fields = '__all__'
        read_only_fields = ['study', 'author']


class PrivateStudyDetailSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_students(self, obj):
        # 외래키를 사용하지 않았을 경우 생각하여
        obj_list = Student.objects.filter(post_id = obj.id, is_accept = True)
        return StudentSerializer(obj_list, many= True).data

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()] # values() 출력 포맷? 이 원하는 형태 아님
    # penalty_students = StudentSerializer(many= True)
    class Meta:
        model = Study
        fields = "__all__"


# 예를 들어 포스트와 댓글 어떻게 특정 짓나 궁금


# 시리얼 라이저는 단순한 요청

# 주문 목록

# 