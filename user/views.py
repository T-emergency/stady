from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.contrib.auth import views as auth_views

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .models import User, UserProfile
import os

# 카카오
from my_settings import SOCIAL_AUTH_KAKAO_CLIENT_ID
from rest_framework_simplejwt.tokens import RefreshToken
import requests

class UserView(APIView):
    def get(self, request):
        users = request.user
        serializer = UserSerializer(users)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserProfile.objects.create(user = user)
            return Response({'msg': '가입완료'}, status=status.HTTP_201_CREATED)
        else:
            data = dict()
            for key in serializer.errors.keys():
                data[key] = f"이미 존재하는 {key} 또는 형식에 맞지 않습니다."
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = User.objects.get(pk=request.user.id)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '저장완료'}, status=status.HTTP_200_OK)
        else:
            data = dict()
            for key in serializer.errors.keys():
                data[key] = f"이미 존재하는 {key} 또는 형식에 맞지 않습니다."
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.delete()
        return Response(status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
KAKAO_CALLBACK_URI = 'http://127.0.0.1:8000/' + 'user/api/kakao/callback/'
client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID
# 카카오
class KakaoView(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                    },
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "redirect_uri": "http://127.0.0.1:5500/index.html",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()

            kakao_email = user_data.get("kakao_account")["email"]
            kakao_nickname = user_data.get("properties")["nickname"]
            # 유저가 카카오 이메일로 로그인하면 토큰 줘야한다. 로그인 프론트 참조
            # 첫로그인이면 이메일 있는지 중복확인

            try:
                exitst_user = User.objects.filter(email=kakao_email).exists()
                if exitst_user:
                    user=User.objects.get(email=kakao_email)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },status=status.HTTP_200_OK
                    )
                else:
                    user=User.objects.create(username = kakao_nickname, email=kakao_email)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },status=status.HTTP_200_OK
                    )
            except:
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


