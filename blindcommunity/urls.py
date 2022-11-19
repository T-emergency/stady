from django.urls import path
from . import views


urlpatterns = [
    path('', views.TopPostAPIView.as_view(), name='index'),
    path('category/<str:category_name>/', views.PostAPIView.as_view(), name='post'),
    path('<int:post_id>/', views.PostDetailAPIView.as_view(), name='post_detail'), 

    path('<int:post_id>/comment/', views.CommentAPIView.as_view(), name='comment'),
    path('<int:post_id>/comment/<int:comment_id>/', views.CommentDetailAPIView().as_view(), name='post_detail'), 

    path('<int:post_id>/like/', views.PostLikeAPIView.as_view(), name='like'), 
    path('<int:post_id>/<int:comment_id>/like/', views.CommentLikeAPIView.as_view(), name='like'), 
    path('search/', views.SearchAPIView.as_view(), name='search'),
]
