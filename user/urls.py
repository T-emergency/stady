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

    #카카오 이메일 생성
    path('kakao/email/<int:kakao_id>/<str:username>/<str:nickname>/',views.kakao_email,name="kakao_email"),

    # 이메일 비밀번호 리셋
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name= "password_reset_complete"),
    # path('reset_password_done/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name= "password_reset_done"),

]
