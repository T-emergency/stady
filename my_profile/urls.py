from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile, name = 'profile'),
    path('studies/', views.study_list, name = 'study_list'),
]