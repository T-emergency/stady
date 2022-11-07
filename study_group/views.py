from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import get_object_or_404
from .models import Study,User,Student,Tag
from rest_framework.views import APIView
from study_group.serializer import StudyListSerializer, StudyDetailSerializer, StudySerializer, StudyCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
# search
from rest_framework import filters
# search 제네릭이용
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework import viewsets
from study_group.models import Study
from study_group.serializer import StudyListSerializer

from rest_framework.pagination import PageNumberPagination
from django.db.models import Q



from django.core.paginator import Paginator

# class StudyView(APIView):

#     def get(self, request, pk, format=None):
#         studies=Study.objects.all()

#         page_number = self.request.query_params.get('page_number ', 1)
#         page_size = self.request.query_params.get('page_size ', 1)

#         paginator = Paginator(studies , page_size)
#         serializer = StudyListSerializer(paginator.page(page_number) , many=True)

#         response = Response(serializer.data, status=status.HTTP_200_OK)
#         return response


from rest_framework.pagination import PageNumberPagination

class StudyView(APIView, PageNumberPagination):
    page_size = 6
    def get(self, request, format=None):
        studies=Study.objects.all()
        results = self.paginate_queryset(studies, request, view=self)
        serializer = StudyListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)



class Search(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search','') #파라미터 가져오기
        list = Study.objects.all()
        if search:
            list = list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
                ).distinct()
            serializer=StudyListSerializer(list,many=True)
        return Response(serializer.data)


class StudyView(APIView):

    def post(self, request):
        content=request.POST.get('tags')
        print(content)
        tag_list=content.split(' ')
        for i in tag_list:
            if '#' in i:
                Tag.tag_name=i
                Tag.save()
            else:
                pass
        serializer = StudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        studies = Study.objects.all()
        print(list)
        serializer = StudyListSerializer(studies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudySearchView(generics.ListAPIView):
        queryset=Study.objects.all()
        serializer_class = StudyListSerializer
        filter_backends=[filters.SearchFilter]
        search_fields=('title',)

class CreateView(APIView):
    def post(self, request):
        pass

class StudyDetailView(APIView):
    def get(self, request, study_id):
        study=get_object_or_404(Study, id=study_id)
        serializer = StudyDetailSerializer(study)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, study_id):
        pass






############################

# def study_detail(request, study_id):
#     study = Study.objects.get(id=study_id)
#     context={
#         'study':study,
#     }
#     return render(request,'study_group/study_detail.html', context)        

def like(request, study_id):
    # 스터디 id에 해당하는 객체를 가져온다
    study = get_object_or_404(Study, pk=study_id)
    # 요청한 사용자
    user = request.user

    # 가져온 스터디의 객체에서 like에 가면 좋아요한 user있을건데(테이블이 있을거임)
    # 요청한 유저가 있는걸 filter함 그럼 필터말고 겟도 가능하지않나?
    filtered_like_study = study.like.filter(id=user.id)

    # 변수를 이용해서 존재할경우, study like 에서 유저 제거 해당 객체를 삭제한다고 이해함
    if filtered_like_study.exists():
        study.like.remove(user) #여기서 user는 뭘 의미하는지 모르겠네 아마 유저인듯 조건에 request.user를 넣는거임
        return redirect('studies:view_study', study_id=study.id)

    # 없을 경우, study 객체에서 like에 해당 user를 추가
    else:
        study.like.add(user)
        return redirect('studies:view_study', study_id=study.id)

def submit(request, study_id):
    user=request.user
    study=get_object_or_404(Study, pk=study_id)

    try:
        student = Student.objects.get(user = user, post = study)
        study.submit.remove(student) # 참여자라고 이해하면 됨 
        student.delete()
        return redirect('studies:view_study', study_id=study.id)

    except Student.DoesNotExist:
        student = Student.objects.create(user = user, post = study)
        study.submit.add(student)
        return redirect('studies:view_study', study_id=study.id)


def index(request):

    if request.method == 'GET':
        
        studys = Study.objects.all()
        content={
            "studys":studys
        }
    return render(request, 'study_group/index.html',content)


# def create_study(request):

#     if request.method == 'GET':
#         return render(request, 'study_group/create.html')

#     if request.method == 'POST':
#         user = request.user
#         title = request.POST.get('title')
#         thumbnail_img = request.FILES.get('image')
#         #TODO headcount가 int혹은 범위 내에 있는지 판별해야함
#         headcount = request.POST.get('headcount')
#         content = request.POST.get('content')

#         Study.objects.create(user = user, title=title,thumbnail_img=thumbnail_img,headcount=headcount,content=content)

#         # study = Study()
#         # study.user = user
#         # study.title = title
#         # study.thumbnail_img = thumbnail_img
#         # study.headcount = headcount
#         # study.content = content
#         # study.save()
#         # return HttpResponse('등록완료')
#         return redirect('studies:studies')
    

def view_study(request, study_id):

    user = request.user
    study_post = Study.objects.get(id=study_id)
    student_list = [student.user for student in Student.objects.filter(post=study_post, is_accept = None)]
    member_list = [student.user for student in Student.objects.filter(post=study_post, is_accept = True)]
    if request.method == 'GET':

        context = {
            'study_post': study_post,
            'student_list': student_list,
            'member_list': member_list,
            'limit_cnt' : study_post.headcount,
            'now_cnt' : study_post.student_set.filter(is_accept = True).count(),
            'is_author' : '',
            'is_student' : '',
            'sended' : '',
        }

        if study_post.user == user: # 주최자일 때
            context['is_author'] = True
        else: # 주최자 x

            is_student = Student.objects.filter(user=user, post=study_post, is_accept = True).exists()
            sended = Student.objects.filter(user=user, post=study_post, is_accept = None).exists()

            if  is_student: # 스터디 참여자
                context['is_student'] = True
            elif sended: # 신청자
                context['sended'] = True


        return render(request, 'study_group/study_detail.html',context)
    
    if request.method == 'POST':
        try:
            Student.objects.get(user = user, post = study_post)
        except Student.DoesNotExist:
            Student.objects.create(user = user, post = study_post, is_accept=None)

        return redirect('studies:view_study', study_id=study_post.id)


def propose_study(request, user_id):
    if request.method == 'GET':
        return render(request, 'study_group/')



def choice(request,user_id, study_id):
    if request.method == 'POST':
        user = request.user
        
        is_accept = request.POST.get('is_choice')
        student = Student.objects.get(user_id=user_id,post_id=study_id)
        student.is_accept = int(is_accept)
        student.save()
        
        return redirect('studies:view_study', study_id=study_id)


def delete_student(request, user_id, study_id):
    if request.method =='POST':
        try:
            student = Student.objects.get(user_id = user_id, post_id=study_id)
            student.delete()
        except Student.DoesNotExist:
            pass
        return redirect('studies:view_study', study_id=study_id)


