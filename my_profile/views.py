from django.shortcuts import render, redirect
from study.models import StudyLog
from user.models import User
from study_group.models import Study, Bookmark

from datetime import datetime, date
from study.serializer import get_day_log, log_to_json
# from django.utils import timezone
# from study.serializer import log_to_json


# Create your views here.

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


    

def study_list(request):
    
    user = request.user
    study_list = Study.objects.filter(user = user)
    bookmark_list = Bookmark.objects.filter(user=user)
    print(study_list)
    
    context ={
        'study_lists' :study_list,
        'bookmark_lists': bookmark_list,
        }
    return render(request, 'user/study_list.html', context)