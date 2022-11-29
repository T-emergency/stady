from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudyLogView.as_view()),
    path('log/', views.GetLogView.as_view()),
    path('todo/', views.ToDoVIew.as_view(), name='todo_views'),
    path('todo/<int:todo_id>/', views.TodoChangeView.as_view(),name='todo_change_view')

]
