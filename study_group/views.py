
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import StudentPost, StudentPostComment, Study, Student, Tag, UserTagLog
from .serializers import (
    PrivateStudentPostDetailSerializer,
    PrivateStudentPostSerializer,
    PrivateStudyAuthorDetailSerializer,
    PrivateStudyDetailSerializer,
    PrivateStudyPostCommentSerializer,
    StudySerializer,
    StudentSerializer,
    StudyDetailSerializer,
)
# search
from rest_framework import filters
# search 제네릭이용
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class Search(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search', '')
        list = Study.objects.all()
        if search:
            list = list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).distinct()
            serializer = StudySerializer(list, many=True)
        return Response(serializer.data)


class StudyListAPIView(APIView, PageNumberPagination):
    permission_classes = [permissions.IsAuthenticated]
    page_size = 6
    def get(self, request):
        studies = Study.objects.order_by('-create_dt')
        recommend_tags = None
        recommend_study = []

        if recommend_tags == None:
            pass
        else:
            for tag in recommend_tags:
                tag = Tag.objects.get(tag_name=tag)
                recommend_studies = tag.tag_studies.order_by("?")[:3]
                for s in recommend_studies:
                    recommend_study.append(s)

        results = self.paginate_queryset(studies, request, view=self)

        serializer = StudySerializer(results, many=True)
        serializer2 = StudySerializer(recommend_study[:3], many=True)

        data = {
            "studies": serializer.data,
            "recommend_studies": serializer2.data
        }
        return self.get_paginated_response(data)

    def post(self, request):
        tags = request.data.get('tags')
        tag_list = []
        print(request.data)

        for i in tags.split(','):
            if i == '' or len(i) >= 13:
                continue
            tag, _ = Tag.objects.get_or_create(tag_name=i.strip())

            tag_list.append(tag.id)

        study = StudySerializer(data=request.data, context={'tags': tag_list})

        if study.is_valid():
            study = study.save(user=request.user)
            Student.objects.create(user = request.user, post = study, is_accept = True)
            return Response(status=status.HTTP_201_CREATED)
        print(study.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudySearchView(generics.ListAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)

class StudyDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, study_id):
        user = request.user
        study = get_object_or_404(Study, pk=study_id)
        tag_list = study.tags.all()

        for tag in tag_list:
            tag_log, _ = UserTagLog.objects.get_or_create(tag=tag, user=user)
            tag_log.count += 1
            tag_log.save()

        recommend_tags = None

        if recommend_tags == None:
            pass
        else:
            recommend_study = []
            for tag in recommend_tags:
                tag = Tag.objects.get(tag_name=tag)
                studies = tag.tag_studies.order_by("?")[:3]
                for s in studies:
                    recommend_study.append(s)

        serializer = StudyDetailSerializer(study, context={'request': request})
        student = Student.objects.filter(post_id=study_id)
        print("참여자: ", student)
        serilaizer3 = StudentSerializer(student, many=True)
        if recommend_tags != None:
            serializer2 = StudySerializer(recommend_study[:9], many=True)
            data = {
                "study_detail": serializer.data,
                "recommend_studies": serializer2.data,
                "student": serilaizer3.data,
            }
            print("recommend_tags 있음")
        else:
            data = {
                "study_detail": serializer.data,
                "recommend_studies": None
            }
            print("recommend_tags 없음")
        return Response(data)


    def put(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        if request.user == study.user:
            serializer = StudySerializer(study, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user)
                print("t성공?!")
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



class StudentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, study_id, student_id):
        student = get_object_or_404(Student, id = student_id)
        if student.post.user.id == request.user.id:
            student.is_accept = True
            student.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다.")

    def delete(self, request, study_id, student_id):
        student = get_object_or_404(Student, id = student_id)
        if student.post.user == request.user:
            student.delete()
            return Response("추방 완료")
        else:
            return Response("권한이 없습니다.")

class StudyProposeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, study_id):
        type = request.GET.get('type', '')
        user = request.user
        study = get_object_or_404(Study, pk=study_id)

        student, _ = Student.objects.get_or_create(post=study, user=user)
        if type == 'propose':
            study.submit.add(student)
        elif type == 'cancle' or type == 'drop':
            study.submit.remove(student)
            student.delete()

        return Response(status=status.HTTP_200_OK)


class StudyLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, study_id):
        user = request.user
        study = get_object_or_404(Study, pk=study_id)

        if study.like.filter(pk=user.id).exists():
            print('unlike')
            study.like.remove(user)
        else:
            print('like')
            study.like.add(user)

        return Response(status=status.HTTP_200_OK)

#-----------------스터디원 전용 페이지 -------------------#
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.viewsets import ModelViewSet

# TODO isAuthenticated 상속 받아서 사용하기
class IsStudent(permissions.BasePermission):
    message = "스터디 참여자만 입장 가능합니다."
    def has_object_permission(self, request, view, obj):
        return obj.student_set.filter(user = request.user ,is_accept = True).exists()


class IsPrivatePostAuthorOrReadOnly(permissions.BasePermission):
    message = "스터디 참여자만 입장 가능합니다."
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            obj = obj.study
            return obj.student_set.filter(user = request.user ,is_accept = True).exists()
        
        self.message = "작성자가 아닙니다."
        return obj.author == request.user
class StudentNumberPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('student_list', data),
            ('page_cnt', self.page.paginator.num_pages),
            ('cur_page', self.page.number),
        ]))


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5
    

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('post_list', data),
            ('page_cnt', self.page.paginator.num_pages),
            ('cur_page', self.page.number),
        ]))



class PrivateStudyView(RetrieveAPIView, ListAPIView, CreateAPIView):
    permission_classes = [IsStudent, permissions.IsAuthenticated]
    serializer_class = PrivateStudentPostSerializer

    def get(self, request, *args, **kwargs):

        community_type = request.GET.get("community-type", '')

        if community_type == 'info': # TODO
            self.serializer_class = PrivateStudyDetailSerializer
            obj = self.get_object()
            if obj.user == request.user:
                self.serializer_class = PrivateStudyAuthorDetailSerializer
            return self.retrieve(request, *args, **kwargs)

        elif community_type == 'album':
            pass

        return self.list(request, *args, **kwargs)


    def get_object(self):
        obj = get_object_or_404(Study, id = self.kwargs["study_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        self.pagination_class = PostPageNumberPagination
        obj = self.get_object()
        return StudentPost.objects.filter(study_id = obj.id).order_by('-create_dt')


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        flag = self.perform_create(serializer)
        if not flag:
            return Response({"message" : "참여자가 아닙니다."},status = status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        study = self.get_object()
        try:
            student = Student.objects.get(user = self.request.user , post = study, is_accept = True)
        except Student.DoesNotExist:
            return False
        serializer.save(study = study, author = self.request.user)
        return True


class PrivateStudyDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = PrivateStudentPostDetailSerializer
    permission_classes = [IsPrivatePostAuthorOrReadOnly, permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(StudentPost, id = self.kwargs["post_id"])
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateStudyPostLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, study_id, post_id):
        user = request.user
        student = Student.objects.filter(is_accept = True, post_id = study_id, user_id = user.id)
        post = get_object_or_404(StudentPost, id = post_id)
        if student.exists():

            student = student[0]
            if post.like.filter(id = student.id):
                post.like.remove(student)
            else:
                post.like.add(student)

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
        


        

class PrivateStudyCommentView(ModelViewSet):
    queryset = StudentPostComment.objects.all()
    serializer_class = PrivateStudyPostCommentSerializer

    def get_object(self):
        self.permission_classes = [IsPrivatePostAuthorOrReadOnly]
        obj = get_object_or_404(StudentPostComment, id = self.kwargs["comment_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        self.permission_classes = [IsStudent]
        post = get_object_or_404(StudentPost, id = self.kwargs["post_id"])
        self.check_object_permissions(self.request, post.study)
        serializer.save(post_id = post.id , author = self.request.user)
        return