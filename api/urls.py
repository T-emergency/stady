from django.urls import path
from . import views


urlpatterns = [
    path('studies/', views.StudyListAPIView.as_view()),
    path('studies/<int:study_id>/', views.StudyDetailAPIView.as_view()),
    path('study/', views.StudyLogView.as_view()),
    path('study/log/', views.GetLogView.as_view()),
    path('study/category/', views.CategoryView.as_view()),
    # path('study/log/', views.GetLogView.as_view()),
]