
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter

from study.utils import get_sub_time
from .recommend import get_recommend_tags

from .models import StudentPost, Study, Student, Tag, UserTagLog
from .serializers import (
    PrivateStudentPostSerializer,
    PrivateStudyDetailSerializer,
    StudySerializer,
    StudentSerializer,
    # StudyCreateSerializer,
    # StudyAuthorSerializer,
    # StudyListSerializer,
    StudyDetailSerializer,
)

# search
from rest_framework import filters
# search 제네릭이용
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.http import JsonResponse


class Search(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search', '')  # 파라미터 가져오기
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
        recommend_tags = None #get_recommend_tags(request)
        recommend_study = []

        # print("rec:", recommend_tags)
        if recommend_tags == None:
            pass
        else:
            for tag in recommend_tags:
                # print("tag:", Tag.objects.get(tag_name=tag))
                tag = Tag.objects.get(tag_name=tag)
                recommend_studies = tag.tag_studies.order_by("?")[:3]
                # print("recommend_studie: ", recommend_studies)
                for s in recommend_studies:
                    recommend_study.append(s)
                # recommend_study.append(*recommend_studies)

        results = self.paginate_queryset(studies, request, view=self)

        serializer = StudySerializer(results, many=True)
        serializer2 = StudySerializer(recommend_study[:3], many=True)

        data = {
            "studies": serializer.data,
            "recommend_studies": serializer2.data
        }
        return self.get_paginated_response(data)

    def post(self, request):
        # print(request.data, 'aaa')
        # print(request.FILES.get('image'))

        tags = request.data.get('tags')
        tag_list = []

        # TODO 유효성 검사 구체화 필요
        for i in tags.split(','):
            if i == '' or len(i) >= 13:
                continue
            # request.data의 요소는 바꾸지 못한다.
            tag, _ = Tag.objects.get_or_create(tag_name=i.strip())

            tag_list.append(tag.id)

        study = StudySerializer(data=request.data, context={'tags': tag_list})

        if study.is_valid():
            study = study.save(user=request.user)  # 여기서 tags = tag_lsit 넣어줘도 똑같은 로직?
            Student.objects.create(user = request.user, post = study, is_accept = True)
            return Response(status=status.HTTP_201_CREATED)
        print(study.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudySearchView(generics.ListAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)

####### TODO db조회를 14번하는(태그 미포함) 것을 줄일 필요 다분############## 심각 수준?
class StudyDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, study_id):
        user = request.user
        study = get_object_or_404(Study, pk=study_id)
        tag_list = study.tags.all()  # 제한을 두던, 효율적으로 저장할 수 있는 방법 알아보기

        for tag in tag_list:
            tag_log, _ = UserTagLog.objects.get_or_create(tag=tag, user=user)
            tag_log.count += 1
            tag_log.save()  # 정크를 사용하면 한꺼번에 저장가능한가?

        recommend_tags = None#get_recommend_tags(request)

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
        # student = get_object_or_404(Student, post_id=study_id)
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
            # print(serializer2.data)
        else:
            data = {
                "study_detail": serializer.data,
                "recommend_studies": None
            }
            print("recommend_tags 없음")
        return Response(data)

        # 뷰셋을 사용하면 자동으로 request를 넘겨줌

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

    # # 기존 study_post의 post요청
    # def post(self, request, study_id):
    #     study = get_object_or_404(Study, id=study_id)
    #     if study.user != request.user:
    #         try:
    #             student = Student.objects.get(user=request.user, post=study)
    #             study.submit.remove(student)  # 참여자라고 이해하면 됨
    #             student.delete()
    #             serializer = StudentSerializer(student)

    #         except Student.DoesNotExist:
    #             student = Student.objects.create(user=request.user, post=study)
    #             study.submit.add(student)
    #             serializer = StudentSerializer(student)

    #         return Response(serializer.data)
    #     return Response("잘못된 접근입니다.")


class StudentView(APIView):
    def get(self, request, study_id, user_id):
        student = get_object_or_404(Student, user_id=user_id, post_id=study_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def post(self, request, study_id, user_id):
        student = get_object_or_404(Student, post_id=study_id, user_id=user_id)
        if student.post.user.id == request.user.id:
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


def create_recommand_csv(request):
    return JsonResponse('dd', safe=False)


class StudyProposeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, study_id):
        type = request.GET.get('type', '')
        # print(type)
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
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, DestroyAPIView
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
    page_size = 10
    

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('post_list', data),
            ('page_cnt', self.page.paginator.num_pages),
            ('cur_page', self.page.number),
        ]))



class PrivateStudyView(RetrieveAPIView, ListAPIView, CreateAPIView):
    # get 요청에 유형을 달리하여 시리얼 라이저와 쿼리를 변경하여 요청
    permission_classes = [IsStudent, permissions.IsAuthenticated]
    serializer_class = PrivateStudentPostSerializer

    def get(self, request, *args, **kwargs):

        community_type = request.GET.get("community-type", '')

        if community_type == 'info': # TODO default를 확실하게 픽스
            self.serializer_class = PrivateStudyDetailSerializer
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
        #TODO 카테고리 album, community
        return StudentPost.objects.filter(study_id = obj.id)


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
            student = Student.objects.get(user_id = self.request.user.id , post_id = study.id)
        except Student.DoesNotExist:
            return False
        serializer.save(study_id = study.id, author_id = student.id)
        return True


class PrivateStudyDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = PrivateStudentPostSerializer
    permission_classes = [IsPrivatePostAuthorOrReadOnly, permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(StudentPost, id = self.kwargs["post_id"])
        self.check_object_permissions(self.request, obj)
        return obj


class PrivateStudyCommentView(ModelViewSet):
    pass