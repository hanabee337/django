from pprint import pprint

import requests
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

from facebook import settings


def login_fbv(request):
    # print('login_fbv')
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id,
    }
    return render(request, 'member/login.html', context)


def logout_fbv(request):
    logout(request)
    return redirect('index')


def login_facebook(request):
    # print(request.GET)
    APP_ID = settings.config['facebook']['app_id']
    SECRET_CODE = settings.config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE,
    )

    # login_fbv에서 페이스북 로그인으로 이동 후,
    # 정상적인 로그인 후 (정상적으로 로그인 시 request.GET에 'code' parameter가 추가됨)
    # redirect_uri를 이용해 다시 login_facebook으로 돌아온 후의 동작
    if request.GET.get('code'):
        # Step 1 : 사용자가 로그인 했다라는 검증
        code = request.GET.get('code')

        # Step 2 : user_access_token(사용자 액세스 토큰) 얻어오기
        # 전달받은 code 값을 이용해서 access_token값을 요청함
        # parameter들을 하기처럼 url에 직접 넣지 말 것.
        # url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?'\
        #     'client_id={app_id}'\
        #     '&redirect_uri={redirect_uri}'\
        #     '&client_secret={app_secret}'\
        #     '&code={code_parameter}'.format(
        #         app_id=app_id,
        #         app_secret=secret_code,
        #         code_parameter=code,
        #         redirect_uri=redirect_uri,
        # )

        # 하기처럼 params로 넘겨줄 것.
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?'
        params = {
            'client_id': APP_ID,
            'redirect_uri': REDIRECT_URI,
            'client_secret': SECRET_CODE,
            'code': code,
        }
        r = requests.get(url_request_access_token, params=params)
        pprint(r.text)
        dict_access_token = r.json()
        USER_ACCESS_TOKEN = dict_access_token['access_token']
        print('USER_ACCESS_TOKEN : %s' % USER_ACCESS_TOKEN)

        # Step 3: debug_token을 얻어오기
        # 유저 액세스 토큰과 앱 엑세스 토큰을 사용해서 토큰 검증을 거친다
        url_debug_token = 'https://graph.facebook.com/debug_token?'
        params = {
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN,
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        pprint(dict_debug_token)
        USER_ID = dict_debug_token['data']['user_id']
        print('USER_ID : %s' % USER_ID)

        # 해당 USER_ID로 graph API에 유저정보를 요청
        url_api_user = 'https://graph.facebook.com/{user_id}'.format(
            user_id=USER_ID
        )
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'picture',
            'email',
        ]
        params = {
            'fields': ','.join(fields),
            'access_token': USER_ACCESS_TOKEN,
        }
        r = requests.get(url_api_user, params)
        dict_user_info = r.json()
        pprint(dict_user_info)

        # 페이스북 유저 ID만으로 인증
        user = authenticate(facebook_id=USER_ID)
        # 페이스북 유저 ID와 graph API에 요청한 dict_user_info로 인증
        # user = authenticate(facebook_id=USER_ID, extra_fields=dict_user_info)
        login(request, user)
        return redirect('index')
