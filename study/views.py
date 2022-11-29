# utils
from study.utils import get_sub_time
from django.utils import timezone
from datetime import datetime, date, timedelta

# drf
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# serializers
from api.serializers import StudyLogSerializer
from .serializers import TodoSerializer

#model
from .models import StudyLog, Todo
from user.models import User

# machine-learning part
from .machine import is_study


class StudyLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        type = request.GET.get('type', '')
        user = request.user
        if type == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if type == 'start':
            try:

                user.studylog_set.get(date=date.today(), end_time=None)
                user.recent_check = timezone.now()
                user.save()
                return Response({'msg': '이미 공부 중'}, status=status.HTTP_200_OK)

            except StudyLog.DoesNotExist:
                StudyLog.objects.create(user=user)

            user.recent_check = timezone.now()
            user.save()
            
            data = self.study_log_with_time(user)

            return Response(data, status=status.HTTP_200_OK)

        elif type == 'finish':
            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
            except StudyLog.DoesNotExist:
                return Response({'msg': '공부 종료'})

            if timezone.now() - timedelta(minutes = 5) >= log.start_time :
                log.end_time = timezone.now()
                log.save()

                user.total_time += get_sub_time(log.start_time, log.end_time)
                user.save()
                data = self.study_log_with_time(user)

            else:
                log.delete()
                data = self.study_log_with_time(user)
                data["message"] = "5분 미만의 공부 로그는 저장이 안됩니다."

            return Response(data, status=status.HTTP_200_OK)

        
    def post(self, request):
        """
        사람인식 part
        """
        user = request.user

        if is_study(request):
            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
                user.recent_check = timezone.now()
                user.save()
                return Response({'msg': '공부중'})

            except StudyLog.DoesNotExist:

                StudyLog.objects.create(user=user)

                data = self.study_log_with_time(user)

            return Response(data, status=status.HTTP_200_OK)

        else:

            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
            except StudyLog.DoesNotExist:
                return Response({'msg': 'None'})

            if timezone.now() - timedelta(minutes = 5) >= log.start_time : # 통과
                log.end_time = timezone.now()
                log.save()

                user.total_time += get_sub_time(log.start_time, log.end_time)
                user.save()
                data = self.study_log_with_time(user)

            else:
                log.delete()
                data = self.study_log_with_time(user)
                data["message"] = "5분 미만의 공부 로그는 저장이 안됩니다."

            return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        메모 처리 put 요청
        """
        log_id = request.data.get('logId', '')
        memo = request.data.get('memoTitle', '')

        if log_id == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        study_log = get_object_or_404(StudyLog, pk=int(log_id))
        serializer = StudyLogSerializer(
            study_log, data={"memo": memo}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request):
        """
        사람인식 처리 과정 중 공부 finish 처리가 되면
        새로 생기는 공부로그를 지우는 delete 요청
        """
        user = request.user

        log_list = StudyLog.objects.filter(
            user=user, date=date.today(), end_time=None)
        for log in log_list:
            log.delete()

        data = self.study_log_with_time(user)

        return Response(data, status=status.HTTP_200_OK)

    def study_log_with_time(self, user):

        study_log_list = user.studylog_set.filter(
            date=date.today()).order_by('start_time')

        serializer = StudyLogSerializer(study_log_list, many=True)
        day_total_time = sum([item["sub_time"] for item in serializer.data])

        data = {
            "study_log_list": serializer.data,
            "day_total_time": day_total_time
        }

        return data


    
class GetLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # TODO
    def get(self, request):
        user = request.user
        print(user)
        day = request.GET.get('day', '')
        log_list = StudyLog.objects.filter(user=user, date=day)
        serializer = StudyLogSerializer(log_list, many=True)

        day_total_time = sum([item["sub_time"] for item in serializer.data])

        data = {
            "study_log_list": serializer.data,
            "day_total_time": day_total_time
        }
        return Response(data)



class ToDoVIew(APIView):
    def post(self, request):
        
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self,request):
        today = date.today()

        start_date = datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day) ,'%Y %m %d')
        end_date = datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day)+" 23:59", '%Y %m %d %H:%M')
        user = request.user
        todo = Todo.objects.filter(user_id = user,  create_at__range=[start_date, end_date])
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)


class TodoChangeView(APIView):

    def put(self, request, todo_id):
        todo = Todo.objects.get(id = todo_id)
        serializer = TodoSerializer(todo, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def delete(self, request, todo_id):

        todo = Todo.objects.get(id = todo_id)
        todo.delete()
        return Response('삭제 성공')

