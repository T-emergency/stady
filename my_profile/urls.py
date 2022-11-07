from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('profile/', views.profile, name = 'profile'),
    path('<int:user_id>/', views.ProfileViews.as_view(), name = 'profile_view'),
    path('<int:user_id>/study/', views.StudyListView.as_view(), name='study_list'),
    path('studylog/', views.StudyLogViews.as_view(), name='study_log'),
    path('daylog/<str:day>/', views.StudyDayLogViews.as_view(), name="day_log"),
    path('memolog/<int:log_id>/', views.MemoView.as_view(), name='memo_view'),
    
]