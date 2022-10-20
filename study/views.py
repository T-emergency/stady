from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# utils
from datetime import datetime, date
from django.utils import timezone
from study.serializer import log_to_json

# models part
from user.models import User
from .models import StudyLog

# machine-learning part
from .machine import is_study


# TODO 하루가 끝나면 공부로그에서 백 마지막 시간을 지정해 준다(11시55분경?)
    # import schedule #pip install schedule
    #schedule.every().day.at("23:55").do('함수')

# TODO 하루 지나고 계속 공부 중일때(check함수에 새로운 공부로그 생성)


@login_required(login_url='user:login')
def index(request):

    user = request.user

    if request.method == "GET":

        study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
        study_log_list = log_to_json(study_log_list)
        context = {
            'study_log_list' : study_log_list
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html')


@login_required(login_url='user:login')
def start_study(request):

    if request.method == 'GET':
        
        user = request.user

        try: # 이미 공부 중일 경우
            log = user.studylog_set.get(date = date.today(), end_time = None)
            
            return JsonResponse({'msg' : '이미 공부 중'})

        except StudyLog.DoesNotExist:

            StudyLog.objects.create(user=user)
            # user.study_set.create()
                            
            study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
            study_log_list = log_to_json(study_log_list)

            return JsonResponse({'study_log_list':study_log_list})


    return JsonResponse({'msg':'올바른 접근 아님'})


@login_required(login_url='user:login')
def finish_study(request):
    
    user = request.user
    
    try:
        log = user.studylog_set.get(date = date.today() ,end_time = None)
    except StudyLog.DoesNotExist:
        return JsonResponse({'msg':'성공'})

    log.end_time = timezone.now()
    log.save()
    study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
    study_log_list = log_to_json(study_log_list)

    return JsonResponse({'study_log_list':study_log_list})

    

@login_required(login_url='user:login')
def check_study(request):

    user = request.user

    if request.method == 'POST':

        if is_study(request): # 사람이 있다
            
            try:

                log = user.studylog_set.get(date = date.today() ,end_time = None)

            except StudyLog.DoesNotExist:

                StudyLog.objects.create(user=user)
                study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
                study_log_list = log_to_json(study_log_list)
                return JsonResponse({'study_log_list':study_log_list})

            except : # 많을 때 방어코드 구현 할 것인지
                pass

        else: # 공부 중이 아닐 때

            try:
                log = user.studylog_set.get(date = date.today(), end_time = None)
            except StudyLog.DoesNotExist:
                return JsonResponse({'msg':'None'}) # 날짜가 바뀐 상태에서도 요청이 오고, 사람이 없다면 아무 일을 할 필요가 없다

            log.end_time = timezone.now()
            log.save()
                
            study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
            study_log_list = log_to_json(study_log_list)


            return JsonResponse({'study_log_list':study_log_list})
        return JsonResponse({'msg':'공부중'})


def get_profile(request):
    pass
