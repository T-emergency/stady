from django.shortcuts import render, redirect
from study.models import StudyLog
from user.models import User

from datetime import datetime, date
# from django.utils import timezone
# from study.serializer import log_to_json

def index(request):
    return render(request, 'index.html')


def profile(request):

    # user = request.user
    # username = User.objects.fliter(username = username)
    
    # user_log = username.studylog_set.all()
    # study_log = user.studylog_set.filter(date = date.today()).order_by('start_time')
    
    
    # context ={
    #     'username': username,
    #     'user_log': user_log,
    # }
    # print (context)
    if request.method =='GET':
        return render(request, 'user/profile.html')