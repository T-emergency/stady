from django.shortcuts import render, redirect
from .models import Study,User,Student
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'study_group/index.html')

def studies(request):
        if request.method == 'GET':
            
            studys = Study.objects.all()
            content={
                "studys":studys
            }
        return render(request, 'study_group/studies.html',content)


def create_study(request):
    if request.method == 'GET':
        return render(request, 'study_group/create.html')

    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        thumbnail_img = request.FILES.get('image')
        headcount = request.POST.get('headcount')
        content = request.POST.get('content')

        Study.objects.create(title=title,thumbnail_img=thumbnail_img,headcount=headcount,content=content)
        return HttpResponse('등록완료')

    
def view_study(request, study_id):
    if request.method == 'GET':
        user = request.user
        study_post = Study.objects.get(id=study_id)
        
        if study_post.user == user:
            # student_list = [student.user for student in Student.objects.filter(post=study_post)]
            student_list = Student.objects.filter(post=study_post)
            context = {
                'study_id': study_post.id,
                'user_id': user.id,
                'study_post': study_post,
                'student_list': student_list,
            }
            return render(request, 'study_group/user_post_admin.html',context)
        else:
            if Student.objects.filter(user=user, post=study_post) :
                student = Student.objects.get(user=user, post=study_post)
            else:
                student = None
            context = {
                'study_id': study_post.id,
                'user_id': user.id,
                'study_post': study_post,
                'student': student,
            }

                
        print('user_id:', user.id,'study_id:', study_post.id)

        return render(request, 'study_group/user_post.html',context)
    
    if request.method == 'POST':
        study_post = Study.objects.get(id=study_id)
        student = Student.objects.create(user= request.user, post=study_post, is_accept=None)
        print(student)
        return redirect('view_study', study_id=study_id)
    

        
def like_study(request, user_id):
    if request.method == 'GET':
        return render(request, 'study_group/')


def propose_study(request, user_id):
    if request.method == 'GET':
        return render(request, 'study_group/')




def choice(request,user_id, study_id):
    if request.method == 'POST':
        user = request.user
        
        print ('user_id:',user_id,'study_id:',study_id)
        is_accept = request.POST.get('is_choice')
        student = Student.objects.get(user_id=user_id,post_id=study_id)
        student.is_accept = is_accept
        student.save()
        
        return redirect('view_study', study_id=study_id)


# def accept(request,user_id):
#     if request.POST.method == 'POST':
#         user = request.user
#         is_accept = request.POST.get('is_accept')
#         student = user.student_set.get(user=user)
#         student.is_accept = is_accept
#         student.save()
        
#         return render(request, 'study_group/user_post_admin.html')

# def reject(request,user_id):
#     if request.POST.method == 'POST':
#         user = request.user
#         is_accept = request.POST.get('is_accept')
#         student = user.student_set.filter(user=user)
#         student.is_accept = is_accept
#         student.save()

#         return render(request, 'study_group/user_post_admin.html')

def delete_student(request, user_id, study_id):
    if request.method =='POST':
        student = Student.objects.get(user_id = user_id, post_id=study_id)
        student.delete()
        return redirect('view_study', study_id=study_id)
