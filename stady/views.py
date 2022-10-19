from django.shortcuts import render, redirect
from study.models import StudyLog
from user.models import User

def index(request):
    return render(request, 'index.html')


def profile(request):

    # user = request.user
    # username = User.objects.fliter(username = username)
    
    # user_log = username.studylog_set.all()
    
    
    # context ={
    #     'username': username,
    #     'user_log': user_log,
    # }
    # print (context)
    if request.method =='GET':
        return render(request, 'user/profile.html')