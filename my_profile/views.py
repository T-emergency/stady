from django.shortcuts import render
from study.models import StudyLog
from user.models import User
from study_group.models import Study


from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StudyLogSerializer, StudyMemoSerializer, UserLogSerializer

from study_group.serializers import StudySerializer


from datetime import date
from study.serializers import get_day_log, log_to_json


def profile(request):
    if request.method == 'GET':
        user = request.user
        study_log_list = user.studylog_set.filter(
            date=date.today()).order_by('start_time')
        study_log_list = log_to_json(study_log_list)
        study_day_list = get_day_log(user)

        context = {
            'username': user.username,
            'date': date.today(),
            'bio': user.bio,
            'profile_image': user.profile_image,
            'study_log_list': study_log_list,
            'study_day_list': study_day_list,
            'total_time': user.total_time,
        }

        return render(request, 'user/profile.html', context)


class ProfileViews(APIView):
    def get(self, request, user_id):
        user = request.user
        print(user)
        userlog = User.objects.get(id=user_id)
        serialize = UserLogSerializer(userlog)
        return Response(serialize.data)


class StudyLogViews(APIView):
    def get(self, request):
        user = request.user
        study_log_all_list = user.studylog_set.all().order_by('start_time')
        profile_image = user.profile_image.url
        print(study_log_all_list)
        serialize_log = StudyLogSerializer(study_log_all_list,  many=True)

        context = {
            'log': serialize_log.data,
            'profile_img': profile_image,

        }
        return Response(context)


# 날짜 하루것만
class StudyDayLogViews(APIView):
    def get(self, request, day):
        user = request.user
        day_log = user.studylog_set.filter(date=day).order_by('start_time')
        serialize_log = StudyLogSerializer(day_log,  many=True)

        day_study_time = sum([item["sub_time"] for item in serialize_log.data])
        context = {
            "day_study_time": day_study_time,
            "serialize_log": serialize_log.data
        }

        return Response(context)


class StudyListView(APIView):
    def get(self, request, user_id):

        study_like = Study.objects.filter(like=user_id)
        studies = Study.objects.filter(user=user_id)

        study_apply = [study.post for study in request.user.student_set.all(
        ) if study.is_accept == None]

        serialize_like = StudySerializer(study_like, many=True)
        serialize_study = StudySerializer(studies, many=True)
        serialize_apply = StudySerializer(study_apply, many=True)

        serializers = {
            'serialize_like': serialize_like.data,
            'serialize_study': serialize_study.data,
            'serialize_apply': serialize_apply.data,
        }
        print("serialize_apply: ", serialize_apply.data)
        return Response(serializers)

    

# 메모 생성
class MemoView(APIView):
    def get(self, request, log_id):
        print('메모 get')
        memo_log = StudyLog.objects.get(id=log_id)
        serialize_log = StudyLogSerializer(memo_log)
        return Response(serialize_log.data)

    def post(self, request, log_id):
        memo_log = StudyLog.objects.get(id=log_id)
        serialize = StudyMemoSerializer(memo_log, data=request.data)
        print(serialize)
        if serialize.is_valid():
            print('메모 is valid')
            serialize.save(user=request.user)
            return Response('저장완료')
        else:
            print('메모 post error')
            return Response(serialize.errors)
