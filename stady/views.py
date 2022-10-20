from django.shortcuts import render, redirect
from study.models import StudyLog
from user.models import User

from datetime import datetime, date
# from django.utils import timezone
# from study.serializer import log_to_json




def profile(request):
    if request.method =='GET':
        return render(request, 'user/profile.html')