from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.TopPostAPIView.as_view(), name='index'),
    path('category/', views.PostAPIView.as_view(), name='post'),
    path('<int:post_id>/', views.PostDetailAPIView.as_view(), name='post_detail'), 

    path('<int:post_id>/comment/', views.CommentAPIView.as_view(), name='comment'),
    path('<int:post_id>/comment/<int:comment_id>/', views.CommentDetailAPIView().as_view(), name='comment_detail'), 

    path('<int:post_id>/like/', views.PostLikeAPIView.as_view(), name='post_like'), 
    path('<int:post_id>/<int:comment_id>/like/', views.CommentLikeAPIView.as_view(), name='comment_like'), 
    path('search/', views.SearchAPIView.as_view(), name='search'),
]
