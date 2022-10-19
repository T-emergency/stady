from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# utils
from datetime import datetime, date

# models part
from user.models import User
from .models import StudyLog, InStudy, OutStudy

# machine-learning part
from .machine import is_study


# TODO 하루가 끝나면 공부로그에서 백 마지막 시간을 지정해 준다(11시55분경?)
    # import schedule #pip install schedule
    #schedule.every().day.at("23:55").do('함수')

# TODO 하루 지나고 계속 공부 중일때(check함수에 새로운 공부로그 생성)


@login_required(login_url='login')
def index(request):

    user = request.user

    if request.method == "GET":

        study_log = user.studylog_set.filter(date = date.today()).order_by('start_time')

        context = {
            'study_log' : study_log
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html')


@login_required(login_url='login')
def start_study(request):

    if request.method == 'GET':
        
        user = request.user

        try: # 이미 공부 중일 경우
            log = user.studylog_set.get(date = date.today(), end_time = None)
            
            return JsonResponse({'msg' : '이미 공부 중'})

        except StudyLog.DoesNotExist:

            StudyLog.objects.create(user=user)
            # user.studylog_set.create()

        return JsonResponse({'msg':'성공'})

    return JsonResponse({'msg':'실패'})


@login_required(login_url='login')
def finish_study(request):
    
    user = request.user
    
    try:
        log = user.studylog_set.get(date = date.today() ,end_time = None)
    except StudyLog.DoesNotExist:
        return JsonResponse({'msg':'성공'})

    log.end_time = datetime.now()
    log.save()

    return JsonResponse({'msg':'수고하셨습니다.'})

    

@login_required(login_url='login')
def check_study(request):

    user = request.user

    if request.method == 'POST':

        if is_study(request): # 사람이 있다
            
            try:

                log = user.studylog_set.get(date = date.today() ,end_time = None)

            except StudyLog.DoesNotExist:

                StudyLog.objects.create(user=user)

                return JsonResponse({'msg':'error'})

            except : # 많을 때 방어코드 구현 할 것인지
                pass

        else: # 공부 중이 아닐 때

            try:
                log = user.studylog_set.get(date = date.today(), end_time = None)

            except StudyLog.DoesNotExist:
                return JsonResponse({'msg':'None'}) # 날짜가 바뀐 상태에서도 요청이 오고, 사람이 없다면 아무 일을 할 필요가 없다

            log.end_time = datetime.now()
            log.save()


    return JsonResponse({'msg':'success'})


def get_profile(request):
    pass