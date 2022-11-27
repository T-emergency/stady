from django.urls import path
from . import views

urlpatterns = [
    #-----CBV View-----#
    path('', views.StudyLogView.as_view()),
    path('log/', views.GetLogView.as_view()),
    path('todo/', views.ToDoVIew.as_view(), name='todo_views'),
    path('todo/<int:todo_id>/', views.TodoChangeView.as_view(),name='todo_change_view')
    #-----FBV View-----#
    # path('start/', views.start_study, name = 'start_study'),
    # path('finish/', views.finish_study, name = 'start_study'),
    # path('check/', views.check_study, name = 'start_study'),
    # path('memo/', views.create_memo, name = 'create_memo'),
    # path('log/', views.get_log, name = 'get_log'),
    # path('callback/', views.callback_log, name = 'callback_log'),
]
