from django.shortcuts import render, redirect
import my_settings
import requests
from django.http import JsonResponse

from study_group.models import Bookmark

from .models import User
from study_group.models import Study
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import auth

import string
import random

# 비밀번호 변경, 회원탈퇴
from django.contrib.auth.hashers import check_password
import re


def join(request):
    if request.method == 'GET':
        return render(request, 'user/join.html')

    elif request.method == 'POST':

        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        # TODO
        username = request.POST.get('username', None)
        # nickname = request.POST.get('nickname', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)

        # 정규표현식으로 email check
        check_email = check_email.match(email)
        if check_email is None:
            return render(request, 'user/join.html', {'error': '이메일 양식이 올바르지 않습니다.'})

        # 입력칸이 빈칸일 때
        if username == '' or password == '' or email == '': # or nickname 
            return render(request, 'user/join.html', {'error': '입력란을 모두 채워주세요'})

        # 입력한 패스워드 값이 맞지 않을때
        if password != password2:
            return render(request, 'user/join.html', {'error': '비밀번호가 일치하지 않습니다.'})

        # 이미 가입한 유저가 있을 때
        exist_user = get_user_model().objects.filter(email=email)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 이메일 계정입니다.'})

        # nickname 중복체크 추가
        # exist_user = get_user_model().objects.filter(nickname=nickname)
        # if exist_user:
        #     return render(request, 'user/join.html', {'error': '이미 가입된 사용자 이름 입니다.'})

        # username 중복체크 추가
        exist_user = get_user_model().objects.filter(username=username)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 사용중인 아이디 입니다.'})

        else:
            User.objects.create_user(
                username=username,
                # nickname=nickname,
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

#nickname 만들어 주는 함수
def make_username():
    _LENGTH = 8 #8자리
    string_pool = string.ascii_lowercase #소문자
    while True:
        result = ''
        for _ in range(_LENGTH):
            result += random.choice(string_pool)
        
        if User.objects.filter(username = result).exists():
            pass
        else:
            break

    return result


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

    except access_token.DoesNotExist:
        return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

    #------토큰을 이용하여 사용자 정보 조회------#
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"},
    )
    #------사용자 정보를 활용---------------#
    profile_json = profile_request.json()
    print(profile_json)


    kakao_id = profile_json.get('id')
    # username = make_username()
    username = profile_json['properties']['nickname'] # 진짜 이름

    if User.objects.filter(kakao_id = kakao_id).exists():
        user = User.objects.get(kakao_id = kakao_id)
        user = User.objects.get(username = profile_json['properties']['nickname'])
        auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    
    try:
        email = profile_json['kakao_account']['email']

    except:
        context = {
            'username' : username,
            'kakao_id' : kakao_id,
        }
        return render(request,'user/kakao_email.html', context)
    

    
        

    User.objects.create_user(
        kakao_id = kakao_id,
        username = username,
        email = email
    )
    # user = User.objects.filter(kakao_id = kakao_id)
    user = User.objects.get(username = username)
    auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')

        
    return redirect('/')

#카카오 이메일 페이지에서 이메일 받아오기

def kakao_email(request, kakao_id, username, nickname):
    if request.method == 'GET':
        return redirect('user:kakao_email')
    
    elif request.method=='POST':
        username =username
        kakao_id = kakao_id
        nickname = nickname
        email = request.POST.get('email')

        print(username, kakao_id, nickname, email)
        exist_user = get_user_model().objects.filter(email=email)
        if not exist_user:
            User.objects.create_user(
                username = username,
                email = email,
                kakao_id = kakao_id,
                nickname = nickname,
            )
            return render(request, 'user/login.html')
        else:
            return JsonResponse({"message": "이미 존재하는 계정입니다."}, status=400)


        

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

# 회원정보 변경

@login_required
def update(request):
    # get 요청시 페이지를 보여준다.
    if request.method == 'GET':
        return render(request, 'user/update.html')
    elif request.method == 'POST':
        # 요청한 유저를 user로 정해준다.
        user = request.user
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        username = request.POST.get('username')
        profile_image = request.FILES.get('image')
        print(profile_image)
        print("image= ", request.FILES)
        # nickname = request.POST.get('nickname')

        # filter 를 활용해서 가져온 인스턴스와 입력한 인스턴스를 비교하는 변수를 만들어준다.
        exist_email = get_user_model().objects.filter(email=email)
        exist_username = get_user_model().objects.filter(username=username)
        # 닉네임은 중복이 불가한 컬럼이다. 회원정보 수정시 원래 닉네임과 같으면 변경이 안되는 걸 막기위한 코드다.


        # TODO
        # 입력한 닉네임과 db에 저장되어있는 닉네임이 중복되고 내 닉네임과 다르다면 에러창을 띄운다.
        if exist_email and user.email != email:
            return render(request, 'user/update.html', {'error': '이미 사용중인 email 입니다.'})
        elif exist_username and user.username != username:
            return render(request, 'user/update.html', {'error': '이미 사용중인 username 입니다.'})
        # 이게 있어야 하는지 의문이다.
        else:
            # user.nickname = nickname
            user.bio = bio
            user.email = email
            user.username = username
            user.profile_image = profile_image
            user.save()
            return redirect('/', username)

# 비밀번호 변경
@login_required
def change_password(request):
    if request.method == "POST":
        # 요청유저 인식
        user = request.user
        origin_password = request.POST["origin_password"]
        #장고가 제공한 기능을 통해서 현재 비밀번호와 신규 비밀번호를 비교한다.
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            #현재 비밀번호와 신규 비밀번호를 비교하고 현재 비밀번호와 신규 비밀번호 확인을 비교하여 오류를 띄워준다.
            if origin_password == confirm_password or new_password == origin_password:
                return render(request, 'user/change_password.html', {'error': '사용하고 있는 비밀번호를 입력하셨습니다.'})
            #새 비밀번호와 새 비밀번호 확인이 같아야 비밀번호를 저장한다.
            elif new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user,
                           backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
            else:
                return render(request, 'user/change_password.html', {'error': '신규 비밀번호와 신규 비밀번호 확인을 똑같이 입력해주세요.'})
        else:
            return render(request, 'user/change_password.html', {'error': '현재 비밀번호가 틀렸습니다.'})
    else:
        return render(request, 'user/change_password.html')


### 로그아웃 ###
@login_required
def logout(request):
    auth.logout(request)
    return redirect('user:login')
# 회원탈퇴

def delete(request):
    if request.method == "POST":
        user=request.user
        email=request.POST.get('email')
        password=request.POST.get('password')
        #장고기능으로 입력비밀번호와 현재비밀번호를 확인

        if check_password(password, user.password):
            email==user.email
            print(email)
            user.delete()
            return redirect('/user/login/')
        elif email!=user.email or password!=user.password:
            return render(request, 'user/delete.html', {'error': '비밀번호와 이메일을 다시 확인하세요.'})
    else:
        return render(request, 'user/delete.html')

    

def study_list(request):
    
    user = request.user
    study_list = Study.objects.filter(user = user)
    bookmark_list = Bookmark.objects.filter(user=user)
    print(study_list)
    
    context ={
        'study_lists' :study_list,
        'bookmark_lists': bookmark_list,
        }
    return render(request, 'user/study_list.html', context)