from django.urls import path
from . import views


urlpatterns = [
    path('post_index/', views.post_index, name='post_index'), 
    path('<int:post_id>/', views.post_detail, name='post_detail'), 
    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'), 
    path('post_create/', views.post_create, name='post_create'), 
    # 작성 누르면 get 창뜨고 post_title, post_content 저장 form있는 html
    # path('post_comment/', views.post_comment, name='post_comment'), # 댓글창에 글적고 작성누르면 post_id와 함께 content 저장
]
#변수가 하나있을때 뭐든 가져와서 .id로 사용한것
