from django.urls import path
from . import views

urlpatterns = [
    # Study URL
    path('test/', views.test),
    path('webcam/', views.webcam.detectme, name = 'webcam'),
    path('frame_save/', views.webcam.frame_save, name = 'frame_save'),
    
]
