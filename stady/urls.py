"""stady URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from study import views
from study_group import views
from user import views as user_views

# 이메일 인증
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('user/', include('user.urls')),
    # path('profile/', include('user.urls')),
    path('study/', include('study.urls')),
    path('community/', include('community.urls')),
    # 커뮤니티

    path('studies/', include('study_group.urls')),
    

    path('profile/', include('my_profile.urls')),
    # path('accounts/', include('allauth.urls')), 
     # kakao로그인 요청을 보낼 url
    path('account/login/kakao/', user_views.kakao_social_login, name='kakao_login'),
    #받은 인가 코드로 접근 토큰을 받아 유저의 정보를 가져올 url
    path('account/login/kakao/callback/', user_views.kakao_social_login_callback, name='kakao_login_callback'),
    path('accounts/', include('allauth.urls')), 
    
    
    # 이메일 비밀번호 리셋
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"), name="password_reset_sent"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_confirm.html"), name= "password_reset_complete"),
    path('reset_password_done/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"), name= "password_reset_done"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)