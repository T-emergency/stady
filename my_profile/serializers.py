from rest_framework import serializers
from study_group.models import Study
from study.models import StudyLog
from study import utils
from user.models import User

class StudyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyLog
        fields = "__all__"

class StudyMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyLog
        fields = ("memo",)



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
        fields = "__all__"


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"