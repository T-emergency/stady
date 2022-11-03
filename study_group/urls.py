from django.urls import path
from . import views

app_name = 'studies'

urlpatterns = [
    path('', views.StudyView.as_view(), name = 'studies'),
    path('<int:study_id>/', views.StudyDetailView.as_view(), name = 'view_study'), # 스터디 모집글 확인
    # path('<int:study_id>/like', views.like, name = 'like'), # 
    # path('<int:study_id>/propose/', views.propose_study, name = 'propose_study'),
    # path('<int:study_id>/submit', views.submit, name = 'submit'),

    path('<int:study_id>/accept/<int:user_id>/', views.StudentView.as_view(), name='accept'),
    # path('<int:study_id>/choice/<int:user_id>', views.choice, name = 'choice'),
    # path('<int:study_id>/delete/<int:user_id>', views.delete_student, name = 'delete_student'),
]