from study import utils
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from study.models import StudyLog
from user.models import User

#-------유저 섹션-----------#


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


#---------유저 관련-----------#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token
#---------끝-----------#

#-------스터디 로그 섹션--------#


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
