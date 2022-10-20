from django.shortcuts import render, redirect
import my_settings
import requests
from django.http import JsonResponse

from .models import User

from django.contrib.auth import get_user_model
from django.contrib import auth
import re

import string
import random



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


def kakao_social_login(request):
    if request.method =='GET':
        client_id = my_settings.KAKAO_CLIENT_ID  #앱키
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback'
        return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        )


def kakao_social_login_callback(request):
    """
    받은 인가 코드, 애플리케이션 정보를 담아 /oath/token/에 post요청하여 접근코드를 받아 처리하는 함수
    """

    try:
        code = request.GET.get('code')
        client_id = my_settings.KAKAO_CLIENT_ID # 앱 키
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback' # 인가 코드를 받은 URI
        token_request = requests.post(
            'https://kauth.kakao.com/oauth/token', {'grant_type': 'authorization_code',
                                                    'client_id': client_id, 'redierect_uri': redirect_uri, 'code': code}
        )
        
        token_json = token_request.json()
        #------------유효성 검증 --------------#
        error = token_json.get('error', None)

        if error is not None:
            print(error)
            return JsonResponse({"message": "INVALID_CODE"}, status=400)
        #-------------받은 토큰---------------#
        access_token = token_json.get("access_token")

        

    except KeyError:
        return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

    # except access_token.DoesNotExist:
    #     return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

    #------토큰을 이용하여 사용자 정보 조회------#
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"},
    )
    #------사용자 정보를 활용---------------#
    profile_json = profile_request.json()
    print(profile_json)

    #딕셔너리 검색부분 궁금

    def make_nickname():
        _LENGTH = 8 #8자리
        string_pool = string.ascii_lowercase #소문자
        result = ''

        for _ in range(_LENGTH):
            result += random.choice(string_pool)
        return result

    
    kakao_id = profile_json.get('id')
    username = profile_json['properties']['nickname']
    email = profile_json['kakao_account']['email']
    nickname = make_nickname()
    

    if User.objects.filter(username = username).exists():
        user = User.objects.get(username = username)
        auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')

    elif User.objects.filter(nickname = nickname).exists():
        nickname = make_nickname()
        
    else:
        User.objects.create_user(
            username =username,
            nickname = nickname,
            email = email
        )
        user = User.objects.get(username = username)
        auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        #error
        #You have multiple authentication backends configured and therefore must provide the `backend` argument or set the `backend` attribute on the user.
    return render(request, 'index.html')


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
            # return render(request, 'user/logintest.html')
            return redirect('/')
        else:
            print('로그인 실패')
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})



