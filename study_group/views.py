from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Study,Student
from .serializers import (
    StudySerializer, 
    StudentSerializer, 
    StudyCreateSerializer,
    StudyAuthorSerializer,
    )


class StudyView(APIView):
    def get(self, requset):
        study = Study.objects.all()
        serializer = StudySerializer(study, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudyCreateSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StudyDetailView(APIView):
    def get(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        print("Detail 접근 ok")
        if study.user == request.user:
            print("작성자입니다")
            serializer = StudyAuthorSerializer(study, context={"user":request.user})
            return Response(serializer.data)
        
        print("참여예정자입니다")
        # serializer = StudySerializer(study)
        serializer = StudyAuthorSerializer(study, context={"user":request.user})
        return Response(serializer.data)
        
    # 게시글 수정
    def put(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if request.user == study.user:
            # student_list = [student.user for student in Student.objects.filter(post=study, is_accept= None)]
            serializer = StudyCreateSerializer(study, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        return Response("권한이 없습니다")
    
    def delete(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if study.user ==request.user:
            study.delete()
            return Response('삭제 완료')
        return Response('권한이 없습니다')
    
    # 기존 study_post의 post요청
    def post(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if study.user != request.user:
            try:
                student = Student.objects.get(user = request.user, post = study)
                study.submit.remove(student) # 참여자라고 이해하면 됨 
                student.delete()
                serializer = StudentSerializer(student)
                
            except Student.DoesNotExist:
                student = Student.objects.create(user = request.user, post = study)
                study.submit.add(student)
                serializer = StudentSerializer(student)

            return Response(serializer.data)
        return Response("잘못된 접근입니다.")
    
    
class StudentView(APIView):
    def get(self, request, study_id, user_id):
        student = get_object_or_404(Student, user_id=user_id, post_id=study_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def post(self, request, study_id, user_id):
        student = get_object_or_404(Student, post_id=study_id,user_id=user_id)
        if student.post.user == request.user:   
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("권한이 없습니다.")

    def delete(self, request, study_id, user_id):
        student = get_object_or_404(Student, user_id=user_id,post_id=study_id)
        if student.post.user == request.user: 
            student.delete()
            return Response("삭제 완료")
        else:
            return Response("권한이 없습니다.")
    



# class StudyDetailView(APIView):
    # def get(self, request, study_id):
    #     study = get_object_or_404(Study, id=study_id)
    #     print("Detail 접근 ok")
    #     if study.user == request.user:
    #         print("작성자입니다")
    #         serializer = StudyAuthorSerializer(study, context={"user":request.user})
    #         # submit = Student.objects.filter(post=study)
    #         # print(dir(submit))
    #         # print(submit.order_by())
    #         # submit_list=[]
    #         # for i in submit:
    #         #     submit_list.append({"id":i.id, "username":i.user.username, "is_accept":i.is_accept })
    #         #     print(i.id,i.user,i.is_accept)
    #         # print (submit_list)
            
    #         # data = {
    #         #     "serializer": serializer.data,
    #         #     "submit_list": submit_list,
    #         # }
            
    #         # print(type(study.user), type(request.user))
    #         return Response(serializer.data)
    #         # return Response(data)
        
    #     print("참여예정자입니다")
    #     serializer = StudySerializer(study)
    #     return Response(serializer.data)
    # def post(self, request, study_id):
    #     study = get_object_or_404(Study, id=study_id)
    #     if study.user != request.user:
    #         # try:
    #         #     student=Student.objects.get(user=request.user, post = study)
    #         #     serializer = StudentSerializer(student)
    #         # except Student.DoesNotExist:
    #         #     student = Student.objects.create(user=request.user, post=study, is_accept=None)
    #         #     serializer = StudentSerializer(student)
    #         try:
    #             student = Student.objects.get(user = request.user, post = study)
    #             study.submit.remove(student) # 참여자라고 이해하면 됨 
    #             student.delete()
    #             serializer = StudentSerializer(student)

    #         except Student.DoesNotExist:
    #             student = Student.objects.create(user = request.user, post = study)
    #             study.submit.add(student)
    #             serializer = StudentSerializer(student)

    #         return Response(serializer.data)
    #     return Response("잘못된 접근입니다.")