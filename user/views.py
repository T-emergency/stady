from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import auth

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
        nickname = request.POST.get('nickname')
        # filter 를 활용해서 가져온 인스턴스와 입력한 인스턴스를 비교하는 변수를 만들어준다.
        exist_nickname = get_user_model().objects.filter(nickname=nickname)
        exist_username = get_user_model().objects.filter(username=username)
        # 닉네임은 중복이 불가한 컬럼이다. 회원정보 수정시 원래 닉네임과 같으면 변경이 안되는 걸 막기위한 코드다.

        # TODO
        # 입력한 닉네임과 db에 저장되어있는 닉네임이 중복되고 내 닉네임과 다르다면 에러창을 띄운다.
        if exist_nickname and user.nickname != nickname:
            return render(request, 'user/update.html', {'error': '이미 사용중인 nickname 입니다.'})
        elif exist_username and user.username != username:
            return render(request, 'user/update.html', {'error': '이미 사용중인 username 입니다.'})
        # 이게 있어야 하는지 의문이다.
        else:
            user.nickname = nickname
            user.bio = bio
            user.email = email
            user.username = username
            user.save()
            return redirect('/', user.username)

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
                return redirect('/user/join/')
            else:
                return render(request, 'user/change_password.html', {'error': '신규 비밀번호와 신규 비밀번호 확인을 똑같이 입력해주세요.'})
        else:
            return render(request, 'user/change_password.html', {'error': '현재 비밀번호가 틀렸습니다.'})
    else:
        return render(request, 'user/change_password.html')


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
            return redirect('/user/join/')
        elif email!=user.email or password!=user.password:
            return render(request, 'user/delete.html', {'error': '비밀번호와 이메일을 다시 확인하세요.'})

    else:
        return render(request, 'user/delete.html')