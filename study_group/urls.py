from django.urls import path, include
from . import views
from . import recommend
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('testviewset', views.PrivateStudyCommentView)

app_name = 'studies'

urlpatterns = [
    path('', views.StudyListAPIView.as_view(), name='list'),
    path('<int:study_id>/', views.StudyDetailAPIView.as_view(),
         name='view_study'),  # 스터디 모집글 확인
    path('<int:study_id>/propose', views.StudyProposeView.as_view()),
    path('<int:study_id>/like', views.StudyLikeView.as_view()),
    path('<int:study_id>/accept/<int:user_id>/',
         views.StudentView.as_view(), name='accept'),
    path('search/', views.Search.as_view(), name='search'),
    path('recommand/', recommend.create_recommand_csv),

    #Only Student generic view section
    # path('<int:study_id>/private/', views.PrivateStudyListView.as_view(), name='only_student_detail'),
    path('<int:study_id>/private/', views.PrivateStudyView.as_view(), name='private_study'),
    path('<int:study_id>/private/<int:post_id>/', views.PrivateStudyDetailView.as_view(), name='private_study_detail'),
    path('<int:study_id>/private/<int:post_id>/comment/', views.PrivateStudyCommentView.as_view({
          'post' : 'create'
     })),
     #TODO view파일에서 직접 설정하기 질문 <int:comment_id>와 설정? 혹은 여기에서 퍼미션 설정 질문
    path('<int:study_id>/private/<int:post_id>/comment/<int:comment_id>/', views.PrivateStudyCommentView.as_view({
          'put' : 'update',
          'delete' : 'destroy'
    })),
#     path('<int:study_id>/private/<int:post_id>/comment/<int:comment_id>', views.PrivateStudyDetailView.as_view(), name='private_study_detail'),
]