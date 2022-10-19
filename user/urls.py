from django.urls import path, include
from . import views

# 이메일 인증
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    # User URL
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('update/', views.update, name='update'),
    # path('change_password/', views.change_password, name='change_password'),

    # 이메일 비밀번호 리셋
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name= "password_reset_complete"),
    # path('reset_password_done/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name= "password_reset_done"),

    # kakao로그인 요청을 보낼 url
    path('account/login/kakao/', views.kakao_social_login, name='kakao_login'),
    #받은 인가 코드로 접근 토큰을 받아 유저의 정보를 가져올 url
    path('account/login/kakao/callback/', views.kakao_social_login_callback, name='kakao_login_callback'),

]
