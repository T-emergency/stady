from django.urls import path
from . import views
from . import recommend


app_name = 'studies'

urlpatterns = [
    path('', views.StudyListAPIView.as_view(), name='list'),
    path('<int:study_id>/', views.StudyDetailAPIView.as_view(),
         name='view_study'),
    path('<int:study_id>/propose/', views.StudyProposeView.as_view()),
    path('<int:study_id>/like/', views.StudyLikeView.as_view()),
    path('<int:study_id>/choose/<int:student_id>/', views.StudentView.as_view()),
    path('search/', views.Search.as_view(), name='search'),
    path('recommand/', recommend.create_recommand_csv),

    path('<int:study_id>/private/', views.PrivateStudyView.as_view(), name='private_study'),
    path('<int:study_id>/private/<int:post_id>/', views.PrivateStudyDetailView.as_view(), name='private_study_detail'),
    path('<int:study_id>/private/<int:post_id>/like/', views.PrivateStudyPostLikeView.as_view()),
    path('<int:study_id>/private/<int:post_id>/comment/', views.PrivateStudyCommentView.as_view({
          'post' : 'create'
     })),
    path('<int:study_id>/private/<int:post_id>/comment/<int:comment_id>/', views.PrivateStudyCommentView.as_view({
          'put' : 'update',
          'delete' : 'destroy'
    })),
]