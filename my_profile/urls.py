from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile, name = 'profile'),
    path('<int:user_id>/study/', views.StudyListView.as_view(), name='study_list'),
    path('<int:user_id>/', views.ProfileViews.as_view(), name='profile'),
]