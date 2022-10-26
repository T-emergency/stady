from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'studies'),
    path('create/', views.create_study, name = 'create_study'), # 스터디 모집글 작성
    path('<int:study_id>/', views.view_study, name = 'view_study'), # 스터디 모집글 확인
    path('<int:study_id>/like', views.like_study, name = 'list_study'), # 
    path('<int:study_id>/propose/', views.propose_study, name = 'propose_study'),
    # path('<int:study_id>/accept/<int:user_id>', views.accept, name = 'accept'),
    # path('<int:study_id>/reject/<int:user_id>', views.reject, name = 'reject'),
    path('<int:study_id>/choice/<int:user_id>', views.choice, name = 'choice'),
    path('<int:study_id>/delete_student/<int:user_id>', views.delete_student, name = 'delete_student'),
]