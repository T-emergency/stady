from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CustomTokenObtainPairView, UserView



app_name = 'user'

urlpatterns = [
    # User URL
    # path('join/', views.join, name='join'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('update/', views.update, name='update'),
    # path('change_password/', views.change_password, name='change_password'),
    # path('delete/', views.delete, name='delete'),

    path('join/', UserView.as_view(), name='user_view'),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
