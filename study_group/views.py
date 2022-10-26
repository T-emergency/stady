from django.shortcuts import get_object_or_404, redirect, render
from .models import Study,User,Student

def study_detail(request, study_id):
    study = Study.objects.get(id=study_id)
    context={
        'study':study,
    }
    return render(request,'study_group/study_detail.html', context)        

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
        study.like.remove(user) #여기서 user는 뭘 의미하는지 모르겠네 아마 유저인듯
        return redirect('study_detail', study_id=study.id)

    # 없을 경우, study 객체에서 like에 해당 user를 추가
    else:
        study.like.add(user)
        return redirect('study_detail', study_id=study.id)

def submit(request, study_id):
    user=request.user
    study=get_object_or_404(Study, pk=study_id)
    filter_submit_study= study.submit.filter(id=user.id)
    if filter_submit_study.exists():
        study.submit.remove(user)
        return redirect('study_detail', study_id=study.id)
    else:
        study.submit.add(user)
        return redirect('study_detail', study_id=study.id)


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


