from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response

# utils
from datetime import datetime, date
from django.utils import timezone
from study.serializers import log_to_json
from study.utils import get_sub_time

# models part
from user.models import User
from .models import StudyLog, Todo

# machine-learning part
from .machine import is_study

from rest_framework.views import APIView

from .serializers import TodoSerializer



# TODO 하루가 끝나면 공부로그에서 백 마지막 시간을 지정해 준다(11시55분경?)
# import schedule #pip install schedule
# schedule.every().day.at("23:55").do('함수')

# TODO 하루 지나고 계속 공부 중일때(check함수에 새로운 공부로그 생성)


@login_required(login_url='user:login')
def index(request):

    user = request.user

    if request.method == "GET":

        study_log_list = user.studylog_set.filter(
            date=date.today()).order_by('start_time')
        study_log_list = log_to_json(study_log_list)
        context = {
            'study_log_list': study_log_list
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html')


@login_required(login_url='user:login')
def start_study(request):

    if request.method == 'GET':

        user = request.user

        try:  # 이미 공부 중일 경우
            log = user.studylog_set.get(date=date.today(), end_time=None)

            return JsonResponse({'msg': '이미 공부 중'})

        except StudyLog.DoesNotExist:

            StudyLog.objects.create(user=user)
            # user.study_set.create()

            study_log_list = user.studylog_set.filter(
                date=date.today()).order_by('start_time')
            study_log_list = log_to_json(study_log_list)

            return JsonResponse({'study_log_list': study_log_list})

    return JsonResponse({'msg': '올바른 접근 아님'})


@login_required(login_url='user:login')
def finish_study(request):

    user = request.user

    try:
        log = user.studylog_set.get(date=date.today(), end_time=None)
    except StudyLog.DoesNotExist:
        return JsonResponse({'msg': '성공'})

    log.end_time = timezone.now()
    log.save()

    user.total_time += get_sub_time(log.start_time, log.end_time)
    user.save()

    study_log_list = user.studylog_set.filter(
        date=date.today()).order_by('start_time')
    study_log_list = log_to_json(study_log_list)

    return JsonResponse({'study_log_list': study_log_list})


@login_required(login_url='user:login')
def check_study(request):

    user = request.user

    if request.method == 'POST':

        if is_study(request):  # 사람이 있다

            try:

                log = user.studylog_set.get(date=date.today(), end_time=None)

                return JsonResponse({'msg': '공부중'})

            except StudyLog.DoesNotExist:

                StudyLog.objects.create(user=user)

                study_log_list = user.studylog_set.filter(
                    date=date.today()).order_by('start_time')
                study_log_list = log_to_json(study_log_list)

                return JsonResponse({'study_log_list': study_log_list})

        else:  # 공부 중이 아닐 때

            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
            except StudyLog.DoesNotExist:
                # 날짜가 바뀐 상태에서도 요청이 오고, 사람이 없다면 아무 일을 할 필요가 없다
                return JsonResponse({'msg': 'None'})

            log.end_time = timezone.now()
            log.save()

            user.total_time += get_sub_time(log.start_time, log.end_time)
            user.save()

            study_log_list = user.studylog_set.filter(
                date=date.today()).order_by('start_time')
            study_log_list = log_to_json(study_log_list)

            return JsonResponse({'study_log_list': study_log_list})

    return JsonResponse({'msg': '잘 못 된 접근이다.'})


@login_required(login_url='user:login')
def create_memo(request):
    user = request.user
    # TODO form을 이용한 유효성 검사
    if request.method == "POST":
        log_id = request.POST.get('logId', '')
        memo_title = request.POST.get('memoTitle', '')

        study_log = StudyLog.objects.get(pk=int(log_id))

        if user != study_log.user:
            return JsonResponse({'msg': '작성권한 없음'})

        study_log.memo = memo_title
        study_log.save()

        return JsonResponse({'msg': '저장 완료'})

    return JsonResponse({'msg': '바르지 않은 접근'})


def get_log(request):
    user = request.user

    if request.method == "GET":
        day = request.GET.get('day', '')

        log_list = [log for log in StudyLog.objects.filter(
            user=user) if log.date.strftime('%Y-%m-%d') == day]
        study_log_list = log_to_json(log_list)

        return JsonResponse({'study_log_list': study_log_list})


def callback_log(request):
    if request.method == 'POST':

        user = request.user

        log_list = StudyLog.objects.filter(
            user=user, date=date.today(), end_time=None)
        for log in log_list:
            print(log)
            log.delete()

        study_log_list = user.studylog_set.filter(
            date=date.today()).order_by('start_time')
        study_log_list = log_to_json(study_log_list)

        return JsonResponse({'study_log_list': study_log_list})

    return JsonResponse({'msg': '올바르지 않은 접근'})



#todo가 들어왓을때
#플러스 버튼을 누르면 추가할 수 있는 input과 버튼이 나타난다
#content에 input값을 받아서 저장 날짜 저장
#profile 페이지에서 get으로 받아올 때 todo.objects.filter(id = user_id).order_by(some)
#근데 오늘 날짜만 나와야 한다 todo.objects.filter(id=user_id ,date = today() )
#아마 데이터가 없으면 에러가 날테니 try/except도 필요할수 있다.


class ToDoVIew(APIView):
    def post(self, request):
        print('todo post 함수 실행')
        
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid():
            print('is valid')
            serializer.save(user = request.user)
            return Response(serializer.data)
        else:
            print('is not valid')
            return Response(serializer.errors)

    def get(self,request):
        print('todo get함수 실행')
        # print(date.today())
        today = date.today()

        start_date = datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day) ,'%Y %m %d')
        end_date = datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day)+" 23:59", '%Y %m %d %H:%M')
        user = request.user
        todo = Todo.objects.filter(user_id = user,  create_at__range=[start_date, end_date])
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)


class TodoChangeView(APIView):
    def put(self, request, todo_id):
        print('put함수 실행')
        print(request.data)
        todo = Todo.objects.get(id = todo_id)
        serializer = TodoSerializer(todo, data = request.data)
        if serializer.is_valid():
            print('is valid')
            serializer.save()
            return Response(serializer.data)
        print('is not valid')
        return Response(serializer.errors)
    
    def delete(self, request, todo_id):
        print('delete함수 실행')
        todo = Todo.objects.get(id = todo_id)
        todo.delete()
        return Response('삭제 성공')

