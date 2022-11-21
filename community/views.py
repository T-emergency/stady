# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from user.models import User
# # from .models import Post, PostComment
# from django.core.paginator import Paginator
# from django.utils import timezone
# from django.http import HttpResponseNotAllowed



# def post_index(request): #인자는request
#     page= request.GET.get('page','1') #페이지를  나누어주는 과정 호출했을때 기준페이지 1 설정
#     post_list=Post.objects.order_by('-create_date')
    
#     paginator = Paginator(post_list, 10)
#     page_obj = paginator.get_page(page)
#     context={'post_list' : page_obj}
#     return render(request, 'community/community.html', context)


# def post_detail(request, post_id):
#     post=Post.objects.get(id=post_id)
#     context={'post' : post}
#     return render(request, 'community/post_detail.html', context)
#     # return redirect('post_detail', post_id = post.id)
# #디테일 안에서 context를 사용할 수 있다.
# #인자=post_id 는 a+b 처럼 쓰려고 가져온것 

# @login_required(login_url='user:login')
# def comment_create(request, post_id):
#     #post만 있는경우?
#     post= get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         content=request.POST.get('content')

#         if content == '':
#             print(post.id)
#             return redirect('post_detail', post_id=post.id)

#         user=request.user
#         print(post)
#         PostComment.objects.create(
#             content = content,
#             user = user,
#             post = post,
#             )

#         # return redirect('post_detail', id = post.id)
#         context = {'post':post}
#         return render(request, 'community/post_detail.html', context)
# #render
# @login_required(login_url='user:login')
# def post_create(request):

#     if request.method == 'POST':

#         user=request.user
#         title=request.POST.get('title')
#         content=request.POST.get('content')
#         Post.objects.create(
#             user=user,
#             title=title,
#             content=content)

#         return redirect('post_index')

#     else:
#         return render(request, 'community/post_create.html')

