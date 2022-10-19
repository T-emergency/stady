from django.shortcuts import render, redirect
from stady.settings import MY_SECRET
import requests
from django.http import JsonResponse
from .models import User


from django.contrib import auth


def index(request):
    return render(request, 'user/index.html')



def kakao_social_login(request):
    if request.method =='GET':
        client_id = MY_SECRET['CLIENT_ID']  #앱키
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback'
        return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        )


def kakao_social_login_callback(request):
    """
    받은 인가 코드, 애플리케이션 정보를 담아 /oath/token/에 post요청하여 접근코드를 받아 처리하는 함수
    """
    print('카카오콜백 함수')

    try:
        code = request.GET.get('code')
        client_id = MY_SECRET['CLIENT_ID'] # 앱 키
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

    #딕셔너리 검색부분 궁금
    kakao_id = profile_json.get('id')
    username = profile_json['properties']['nickname']
    email = profile_json['kakao_account']['email']


    if User.objects.filter(username = username).exists():
        user = User.objects.get(username = username)
        auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        
    else:
        User.objects.create_user(
            username =username,
            # password = '7009900', #이 값이 없어도 가입이 가능
            email = email
        )
        user = User.objects.get(username = username)
        auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        #error
        #You have multiple authentication backends configured and therefore must provide the `backend` argument or set the `backend` attribute on the user.
    return render(request, 'user/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')



