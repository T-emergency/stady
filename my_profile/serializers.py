from rest_framework import serializers
from study_group.models import Study
from study.models import StudyLog
from study import utils

class StudyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = "__all__"



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

