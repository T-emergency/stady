from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user.models import User
from django.shortcuts import render
from .models import Post


# Create your views here.

@login_required(login_url='user:login')
def post(request):

    user=request.user

    if request.method == "GET":
        return render(request, 'community/community.html/')

def post_index(request):
    post_list=Post.objects.order_by('-create_date')
    context={'post_list' : post_list}
    return render(request, 'community/community.html', context)

def post_detail(request, post_id):
    post=Post.objects.get(id=post_id)
    context={'post' : post}
    return render(request, 'community/post_detail.html', context)

# @login_required(login_url='user:login')
# def index(request):

#     user = request.user

#     if request.method == "GET":

#         study_log_list = user.studylog_set.filter(date = date.today()).order_by('start_time')
#         type(study_log_list)
#         study_log_list = log_to_json(study_log_list)
#         context = {
#             'study_log_list' : study_log_list
#         }
#         return render(request, 'index.html', context)

#     return render(request, 'index.html')


# def post_create(request):

#     user=user.request
#     pass

# def post(request, post_id):
#     post_title = get_object_or_404(Post, pk=post_id)
#     context = {'question': question}
#     return render(request, 'pybo/question_detail.html', context)
#     #question get 은 질문id만 가져온다. id 가져온다 그 id를 보내주는데
#     #id=question_id 이름 정해주고 그걸 전달 context로
#     #왜 html에서 question. 으로 사용가능하냐 id로 넘어가는데
#     #하나의 객체를 들고온다