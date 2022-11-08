from django.urls import path
from . import views


urlpatterns = [
    path('study/', views.StudyLogView.as_view()),
    path('study/log/', views.GetLogView.as_view()),
    path('study/category/', views.CategoryView.as_view()),
]
