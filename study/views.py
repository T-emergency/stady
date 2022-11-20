from study.machine import is_study
from study.models import StudyLog
from study.utils import get_sub_time
from django.utils import timezone
from datetime import datetime, date
from user.models import User
from django.shortcuts import render, get_object_or_404

# drf
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# serializers
from api.serializers import StudyLogSerializer

# machine-learning part
from .machine import is_study


# TODO 하루가 끝나면 공부로그에서 백 마지막 시간을 지정해 준다(11시55분경?)
    # import schedule #pip install schedule
    #schedule.every().day.at("23:55").do('함수')

# TODO 하루 지나고 계속 공부 중일때(check함수에 새로운 공부로그 생성)


class StudyLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        type = request.GET.get('type', '')
        user = request.user
        if type == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if type == 'start':
            # TODO 프론트에서 is_running플래그를 통해 막음, 또한 페이지 이탈 시 공부 종료 기능 구현 시 필요없을 확률 높아짐
            try:  # 이미 공부 중일 경우

                user.studylog_set.get(date=date.today(), end_time=None)
                user.recent_check = timezone.localtime()
                user.save()
                return Response({'msg': '이미 공부 중'}, status=status.HTTP_200_OK)

            except StudyLog.DoesNotExist:
                StudyLog.objects.create(user=user)

            user.recent_check = timezone.localtime()
            user.save()
            # study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')

            # serializer = StudyLogSerializer(study_log_list, many = True)
            # day_total_time = sum([ item["sub_time"] for item in serializer.data])

            # data = {
            #     "study_log_list" : serializer.data,
            #     "day_total_time" : day_total_time
            # }
            data = self.study_log_with_time(user)

            return Response(data, status=status.HTTP_200_OK)

        elif type == 'finish':
            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
            except StudyLog.DoesNotExist:
                return Response({'msg': '공부 종료'})

            log.end_time = timezone.now()
            log.save()

            user.total_time += get_sub_time(log.start_time, log.end_time)
            user.save()

            data = self.study_log_with_time(user)
            return Response(data, status=status.HTTP_200_OK)

    # check start end >> 마지막에 공부 로그를 뿌려주는 행위는 비슷
    def post(self, request):
        """
        사람인식 part
        """
        user = request.user

        if is_study(request):  # 사람이 있다
            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
                user.recent_check = timezone.localtime()
                user.save()
                return Response({'msg': '공부중'})

            except StudyLog.DoesNotExist:

                StudyLog.objects.create(user=user)

                data = self.study_log_with_time(user)

            return Response(data, status=status.HTTP_200_OK)

        else:  # 공부 중이 아닐 때(check를 하지만 사람이 없다)

            try:
                log = user.studylog_set.get(date=date.today(), end_time=None)
            except StudyLog.DoesNotExist:
                # 날짜가 바뀐 상태에서도 요청이 오고, 사람이 없다면 아무 일을 할 필요가 없다
                return Response({'msg': 'None'})

            log.end_time = timezone.now()
            log.save()

            user.total_time += get_sub_time(log.start_time, log.end_time)
            user.save()

            data = self.study_log_with_time(user)

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

    # TODO 달력을 만든다면 년도와 월을 인자로 받아서 해야하나 고민
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
