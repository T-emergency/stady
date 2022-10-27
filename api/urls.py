from django.urls import path
from . import views


urlpatterns = [
    path('studies/', views.StudyListAPIView.as_view()),
    path('studies/<int:study_id>/', views.StudyDetailAPIView.as_view()),
]
