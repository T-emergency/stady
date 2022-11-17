from django.urls import path
from . import views


urlpatterns = [
   path('<str:category>/', views.BlindPostView.as_view(), name="blind_post_view"),
   path('detail/<int:post_id>/', views.BlindPostDetailView.as_view(), name="blind_post_detail_view"),
   path('comment/<int:post_id>/', views.BlindComment.as_view(),name='blind_comment_view'), 
   path('comment/<int:comment_id>/', views.BlindCommentChange.as_view(), name='blind_comment_change_view'),
]