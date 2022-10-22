from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
# Create your views here.

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