from django.shortcuts import render, redirect
from .models import Study,User,Student
from django.http import HttpResponse

# Create your views here.

def index(request):

    if request.method == 'GET':
        
        studys = Study.objects.all()
        content={
            "studys":studys
        }
    return render(request, 'study_group/index.html',content)


def create_study(request):
    if request.method == 'GET':
        return render(request, 'study_group/create.html')

    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        thumbnail_img = request.FILES.get('image')
        headcount = request.POST.get('headcount')
        content = request.POST.get('content')

        Study.objects.create(user = user, title=title,thumbnail_img=thumbnail_img,headcount=headcount,content=content)

        # study = Study()
        # study.user = user
        # study.title = title
        # study.thumbnail_img = thumbnail_img
        # study.headcount = headcount
        # study.content = content
        # study.save()
        # return HttpResponse('등록완료')
        return redirect('studies:studies')
    

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

        
def like_study(request, user_id):
    if request.method == 'GET':
        return render(request, 'study_group/')


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


