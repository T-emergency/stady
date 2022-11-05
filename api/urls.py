from django.urls import path
from . import views
from . import recommend


urlpatterns = [
    path('studies/', views.StudyListAPIView.as_view()),
    path('studies/<int:study_id>/', views.StudyDetailAPIView.as_view()),
    path('studies/<int:study_id>/propose', views.StudyProposeView.as_view()),
    path('studies/<int:study_id>/like', views.StudyLikeView.as_view()),
    path('study/', views.StudyLogView.as_view()),
    path('study/log/', views.GetLogView.as_view()),
    path('study/category/', views.CategoryView.as_view()),
    # path('study/log/', views.GetLogView.as_view()),
    path('recommand/', recommend.create_recommand_csv),
    # path('recommand/get/', views.get_recommend_tags),
]