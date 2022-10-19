from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    # Study URL
    path('test/', views.test),
    path('webcam/', views.webcam.detectme, name = 'webcam'),
    path('frame_save/', views.webcam.frame_save, name = 'frame_save'),
    
]
=======
    path('start/', views.start_study, name = 'start_study'),
    path('finish/', views.finish_study, name = 'start_study'),
    path('check/', views.check_study, name = 'start_study'),
]
>>>>>>> upstream/feature/study
