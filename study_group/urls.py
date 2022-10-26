from django.urls import path
from . import views

app_name = 'studies'

urlpatterns = [
    path('', views.index, name = 'studies'),
    path('/<int:study_id>', views.view_study, name = 'view_study'), # 스터디 모집글 확인
    path('<int:study_id>', views.study_detail, name ='study_detail'),
    path('<int:study_id>/like', views.like, name = 'like'),
    path('<int:study_id>/submit', views.submit, name = 'submit'),
    path('create/', views.create_study, name = 'create_study'), # 스터디 모집글 작성
    path('', views.studies, name = 'studies')
    # path('/<int:study_id>/propose', views.propose_study, name = 'propose_study'),
]