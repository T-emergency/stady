from django.urls import path
from . import views


urlpatterns = [
    path('', views.StudyListAPIView.as_view()),
    path('<int:study_id>/', views.StudyDetailAPIView.as_view()),
]
