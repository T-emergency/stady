from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.contrib.auth import views as auth_views

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .models import User

# Create your views here.

class UserView(APIView):
    def get(self, request):
        users = request.user
        serializer = UserSerializer(users)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'가입완료'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg" : f"{serializer.errors}"}, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request): # 회원 정보 저장 ( 관심 분야, 닉네임, 이메일 변경?)
        user = User.objects.get(pk = request.user.id)
        serializer = UserSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'저장완료'}, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response({"msg" : f"{serializer.errors}"}, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            user = User.objects.get(pk = request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.delete()
        return Response(status=status.HTTP_200_OK)

        


from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# class MockView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         print(request.user)
#         return Response('get rq')