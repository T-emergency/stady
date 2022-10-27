from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import StudyDetailSerializer, StudySerializer
from study_group.models import Study

from api import serializer
# Create your views here.

# def study_to_json(user, obj_list):
#     study_list = []

#     for study in obj_list:
#         study_dict = {
#             "id" : study.id,
#             "headcount" : study.headcount,
#             "content" : study.content,

#             "now_count" : study.student_set.filter(is_accept = True).count(), # 현재 참여자
#             "is_like" : '',
#             "is_author" : '',
#             "is_student" : '', # 스터디 참여자
#             "sended" : '', # 요청을 보냈냐
#         }
#         is_like = study.like.filter(id = user.id).exists() # True None 반환하는 것을 그대로 넣어도 될지 질문
#         is_student = study.student_set.filter(user = user, post = study, is_accept = True).exists()
#         sended = study.student_set.filter(user = user, post = study, is_accept = None).exists()
#         if study.user == user:
#             study_dict["is_author"] = True

#         elif is_student:
#             study_dict["is_student"] = True

#         elif sended:
#             study_dict["sended"] = True

#         if is_like:
#             study_dict["is_like"] = True

#     return study_list


class StudyListAPIView(APIView):

    def get(self, request):

        studies = Study.objects.all()
        serializer = StudySerializer(studies, many = True)

        return Response(serializer.data)

    def post(self, request):
        request.data["user"] = request.user.id
        study = StudySerializer(data = request.data, context = {'request' : request})
        if study.is_valid():
            study.save()
            return Response(study.data,  status=status.HTTP_201_CREATED)
        return Response(study.errors, status=status.HTTP_400_BAD_REQUEST)

class StudyDetailAPIView(APIView):

    def get(self, request, study_id):
        user = request.user
        study = get_object_or_404(Study, pk = study_id)

        serializer = StudyDetailSerializer(study, context = {'request' : request})
        return Response(serializer.data)

        # 뷰셋을 사용하면 자동으로 request를 넘겨줌