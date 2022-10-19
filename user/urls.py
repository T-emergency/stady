from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [ 
    path('', views.index, name='index'),
    path('login/', views.login , name = 'login'),
    
    # kakao로그인 요청을 보낼 url
    path('account/login/kakao/', views.kakao_social_login, name='kakao_login'),
    #받은 인가 코드로 접근 토큰을 받아 유저의 정보를 가져올 url
    path('account/login/kakao/callback/', views.kakao_social_login_callback, name='kakao_login_callback'),
]
