# utils
from . import utils
from .models import User,Todo

#drf
from rest_framework import serializers

# models
from study.models import StudyLog

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


class TodoSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()

    def get_create_at(self, obj):
        return str(obj.create_at)[:10]

    class Meta:
        model = Todo
        fields = ('content', 'is_checked', 'create_at','id')
        read_only_fields=('user',) 




def log_to_json(study_log_list: list):
    """
    StudyLog의 객체들을 json형식으로 보내기 위한 직렬화 함수
    인자에는 스터디 로그의 
    """
    log_list = []

    for log in study_log_list:
        log_dict = {
            'id': log.id,
            'start_time': utils.get_now_time(log.start_time),
            'end_time': utils.get_now_time(log.end_time),
            'memo': log.memo,
            'date': log.date,
            'sub_time': utils.get_sub_time(log.start_time, log.end_time)
        }

        log_list.append(log_dict)

    return log_list


def get_day_log(user):
    """
    공부한 이력이 있는 날짜들을 가져오는 함수
    """
    study_day_list = sorted(
        set([day.date.strftime('%Y-%m-%d') for day in user.studylog_set.all()]))

    return study_day_list
