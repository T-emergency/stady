from django.shortcuts import render, redirect
from study.models import StudyLog
from user.models import User

from datetime import datetime, date
from study.serializer import log_to_json
# from django.utils import timezone
# from study.serializer import log_to_json

def index(request):
    return render(request, 'index.html')


def profile(request,nickname):

    if request.method =='GET':
        user = request.user
        study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
        study_log_list= log_to_json(study_log_list)
        
        context ={
            'username': user.username,
            'study_log_list': study_log_list,
        }
        print (context)
        return render(request, 'user/profile.html', context)