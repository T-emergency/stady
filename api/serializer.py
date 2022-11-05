from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from study.models import StudyLog
from study_group.models import Study, Student, Tag
from user.models import User

#-------유저 섹션-----------#
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']



#-------스터디 그룹 섹션 -----------#

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "user","title","content", "is_online", "now_cnt","headcount", "thumbnail_img", "tags"]

    user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField() # readonly fields
    now_cnt = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
        
    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept = True).count() + 1

    def create(self, validated_data):
        validated_data['tags'] = self.context['tags']

        instance = super().create(validated_data)
        return instance

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fileds = ['name',]

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
        flag = obj.like.filter(id = self.context.get('request').user.id).exists()
        return flag

    def get_is_author(self, obj):
        flag = False
        if obj.user == self.context.get('request').user:
            flag = True
        return flag

    def get_is_student(self, obj):
        flag = obj.student_set.filter(user = self.context.get('request').user, post = obj, is_accept = True).exists()
        return flag

    def get_sended(self, obj):
        flag = obj.student_set.filter(user = self.context.get('request').user, post = obj, is_accept = None).exists()
        return flag

    def get_thumbnail_img(self, obj):
        return obj.thumbnail_img.url

    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept = True).count() + 1
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Study
        fields = ['id', 'user','headcount','title', 'content','is_online', 'is_like', 'thumbnail_img','is_author', 'is_student', 'sended', 'now_cnt', 'tags']
        read_only_fields = ['tags', ]


# class StudyCreateSerializer(serializers.Serializer):
#     study = StudySerializer()
#     tags = TagSerializer(many= True)

#---------유저 관련-----------#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token
#---------끝-----------#

#-------스터디 로그 섹션--------#

from study import utils
class StudyLogSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    sub_time = serializers.SerializerMethodField()


    def get_start_time(self, obj):
        return utils.get_now_time(obj.start_time)

    def get_end_time(self, obj):
        return utils.get_now_time(obj.end_time)
    
    def get_sub_time(self, obj):
        return utils.get_sub_time(obj.start_time, obj.end_time)
    class Meta:
        model = StudyLog
        fields = '__all__'
        # read_only_fields = ['user',] # 이것이 있으면 partial= True 필요 x

class StudyMonthSerializer(serializers.ModelSerializer):

    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_date(self, obj):
        return

    def get_time(self, obj):
        return
    class Meta:
        model = User
        fields = ['date', 'time']


#------------끝-----------#