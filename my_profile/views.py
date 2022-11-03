from django.shortcuts import render, redirect
from study.models import StudyLog
from user.models import User
from study_group.models import Study
from rest_framework.generics import get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from .serializers import StudyListSerializer


from datetime import datetime, date
from study.serializer import get_day_log, log_to_json


def profile(request):
    if request.method =='GET':
        user = request.user
        study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
        study_log_list= log_to_json(study_log_list)
        study_day_list = get_day_log(user)

        context ={
            'username': user.username,
            'date' : date.today(),
            'bio': user.bio,
            'profile_image': user.profile_image,
            'study_log_list': study_log_list,
            'study_day_list' : study_day_list,
            'total_time' : user.total_time,
        }

        return render(request, 'user/profile.html', context)


    
class StudyListView(APIView):
    #좋아요 한 스터디
    #내가 등록한 스터디
    #등록 대기중인 스터디
    def get(self, request, user_id):
        study_like= Study.objects.filter(like = user_id)#모든 스터디 가져와
        studies = Study.objects.filter(user = user_id)
        study_apply = Study.objects.filter(submit= user_id)
    
        serialize_like = StudyListSerializer(study_like, many=True)
        serialize_study = StudyListSerializer(studies, many=True)
        serialize_apply = StudyListSerializer(study_apply, many=True)

        # serializers = {
        #     'serialize_like':serialize_like.data,
        #     'serialize_study':serialize_study.data,
        #     'serialize_apply':serialize_apply.data,
        # }
        serializers = {
            'serialize_like':serialize_like.data,
            'serialize_study':serialize_study.data,
            'serialize_apply':serialize_apply.data,
        }
       
        return Response(serializers)
