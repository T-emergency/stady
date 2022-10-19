from django.shortcuts import render, redirect
from .models import User
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import auth


import re
# import requests
# import random
# import string

def join(request):
    if request.method == 'GET':
        return render(request, 'user/join.html')

    elif request.method == 'POST':

        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        # TODO
        username = request.POST.get('username', None)
        nickname = request.POST.get('nickname', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)

        # 정규표현식으로 email check
        check_email = check_email.match(email)
        if check_email is None:
            return render(request, 'user/join.html', {'error': '이메일 양식이 올바르지 않습니다.'})

        # 입력칸이 빈칸일 때
        if username == '' or nickname == '' or password == '' or email == '':
            return render(request, 'user/join.html', {'error': '입력란을 모두 채워주세요'})

        # 입력한 패스워드 값이 맞지 않을때
        if password != password2:
            return render(request, 'user/join.html', {'error': '비밀번호가 일치하지 않습니다.'})

        # 이미 가입한 유저가 있을 때
        exist_user = get_user_model().objects.filter(email=email)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 이메일 계정입니다.'})

        # nickname 중복체크 추가
        exist_user = get_user_model().objects.filter(nickname=nickname)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 사용자 이름 입니다.'})

        # username 중복체크 추가
        exist_user = get_user_model().objects.filter(username=username)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 성명 입니다.'})

        else:
            User.objects.create_user(
                username=username,
                nickname=nickname,
                password=password,
                email=email,
            )
            return render(request, 'user/login.html')

### 로그인 ###
# def login(request):
#     user=request.user
#     email = request.POST.get('email', None)
#     password = request.POST.get('password', None)
#     if request.method == 'GET':
#         return render(request, 'user/login.html')
#     elif request.method == 'POST':
#         user = auth.authenticate(request, email=email, password=password)
#         if user is not None:
#             auth.login(request, user)
#             print(email)  # 로그인 처리
#             user = request.user
#             print(user.nickname, user, user.username)
#             return render(request, 'user/logintest.html')
#     else:
#         return render(request, 'user/logintest.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        # 이메일 양식 체크
        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        check_email = check_email.match(email)

        if check_email is None:
            return render(request, 'user/login.html', {'error': '이메일 양식이 올바르지 않습니다.'})

        # 입력란 빈칸일때
        if email == '':
            return render(request, 'user/login.html', {'error': '메일을 입력해주세요.'})
        elif password == '':
            return render(request, 'user/login.html', {'error': '패스워드를 입력해주세요.'})

        # 존재하지 않는 이메일로 로그인 할 경우 에러가 발생하는걸 막기위한 코드
        exist_email = get_user_model().objects.filter(email=email)
        if exist_email:
            pass
        else:
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})
        username = User.objects.get(email=email.lower()).username

        # User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 로그인 처리
            user = request.user
            print(user.username)
            return render(request, 'user/logintest.html')
        else:
            print('로그인 실패')
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})



