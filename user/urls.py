from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CustomTokenObtainPairView, UserView, KakaoView
# from . import fbv_views
app_name = 'user'

urlpatterns = [
    # User URL
    # path('join/', views.join, name='join'),
    # path('login/', fbv_views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('update/', views.update, name='update'),
    # path('change_password/', views.change_password, name='change_password'),
    # path('delete/', views.delete, name='delete'),
    # path('kakao/', views.kakao_login, name='kakao'),

    path('', UserView.as_view(), name='user_view'),
    path('api/token/', CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/kakao/callback/', KakaoView.as_view(), name='kakao_login'),
    
]
