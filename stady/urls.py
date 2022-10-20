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
from .views import profile
from study import views
from user import views as view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('user/', include('user.urls')),
    # path('profile/', include('user.urls')),
    path('study/', include('study.urls')),

    # kakao로그인 요청을 보낼 url
    path('account/login/kakao/', view.kakao_social_login, name='kakao_login'),
    #받은 인가 코드로 접근 토큰을 받아 유저의 정보를 가져올 url
    path('account/login/kakao/callback/', view.kakao_social_login_callback, name='kakao_login_callback'),
    
    # test urls
    path('profile/', profile, name='profile'),
    # path('accounts/', include('allauth.urls')), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

