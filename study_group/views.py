
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

from .models import Study, Student, Tag
from .serializers import (
    StudySerializer,
    StudentSerializer,
    # StudyCreateSerializer,
    StudyAuthorSerializer,
    StudyListSerializer,
)

# search
from rest_framework import filters
# search 제네릭이용
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class StudyView(APIView, PageNumberPagination):
    page_size = 6

    def get(self, request, format=None):
        studies = Study.objects.all()
        results = self.paginate_queryset(studies, request, view=self)
        serializer = StudyListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class Search(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search', '')  # 파라미터 가져오기
        list = Study.objects.all()
        if search:
            list = list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).distinct()
            serializer = StudyListSerializer(list, many=True)
        return Response(serializer.data)


class StudyView(APIView):
    def post(self, request):
        serializer = StudySerializer(
            data=request.data, context={"request": request})
        print(request.user)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("errors: ", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        studies = Study.objects.all()
        serializer = StudySerializer(studies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudySearchView(generics.ListAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)


class StudyDetailView(APIView):
    def get(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        print("Detail 접근 ok")
        if study.user == request.user:
            print("작성자입니다")
            serializer = StudyAuthorSerializer(
                study, context={"user": request.user})
            return Response(serializer.data)

        print("참여예정자입니다")
        # serializer = StudySerializer(study)
        serializer = StudyAuthorSerializer(
            study, context={"user": request.user})
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if request.user == study.user:
            # student_list = [student.user for student in Student.objects.filter(post=study, is_accept= None)]
            serializer = StudySerializer(study, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        return Response("권한이 없습니다")

    def delete(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if study.user == request.user:
            study.delete()
            return Response('삭제 완료')
        return Response('권한이 없습니다')

    # 기존 study_post의 post요청
    def post(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if study.user != request.user:
            try:
                student = Student.objects.get(user=request.user, post=study)
                study.submit.remove(student)  # 참여자라고 이해하면 됨
                student.delete()
                serializer = StudentSerializer(student)

            except Student.DoesNotExist:
                student = Student.objects.create(user=request.user, post=study)
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
        student = get_object_or_404(Student, post_id=study_id, user_id=user_id)
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
        student = get_object_or_404(Student, user_id=user_id, post_id=study_id)
        if student.post.user == request.user:
            student.delete()
            return Response("삭제 완료")
        else:
            return Response("권한이 없습니다.")


# def like(request, study_id):
#     # 스터디 id에 해당하는 객체를 가져온다
#     study = get_object_or_404(Study, pk=study_id)
#     # 요청한 사용자
#     user = request.user

#     # 가져온 스터디의 객체에서 like에 가면 좋아요한 user있을건데(테이블이 있을거임)
#     # 요청한 유저가 있는걸 filter함 그럼 필터말고 겟도 가능하지않나?
#     filtered_like_study = study.like.filter(id=user.id)

#     # 변수를 이용해서 존재할경우, study like 에서 유저 제거 해당 객체를 삭제한다고 이해함
#     if filtered_like_study.exists():
#         study.like.remove(user) #여기서 user는 뭘 의미하는지 모르겠네 아마 유저인듯
#         return redirect('studies:view_study', study_id=study.id)

#     # 없을 경우, study 객체에서 like에 해당 user를 추가
#     else:
#         study.like.add(user)
#         return redirect('studies:view_study', study_id=study.id)
