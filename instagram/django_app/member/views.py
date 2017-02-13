"""
1. def login view를 마만들고
2. member app을 include 잉용해서
    /instagram/urls.py와 member/urls.py 모두 사용
3. login 뷰는 member/login URL과 연결되도록 member/urls.py 구현
4. login 뷰에서는 member/login.html 파일을 구현
5. settings.py에 TEMPLATES_DIR 변수를 할당하고 (os.path.join(BASE_DIR, 'templates'))
    TEMPLATES 설정의 DIRS에 추가
"""
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

from member.forms import LoginForm


def login(request):
    print('login')

    """
    request.method == POST일 때와
    아닐 때읜 동작을 구분
    POST 일 때는 authenticate login을 거치는 로직을 구현
    GET일 때는 member/login.html 을 render하여 return 하도록 함
    """
    if request.method == 'POST':
        # Mission
        # html파일에서 POST요청을 보내기 위해
        # form을 정의하고, input 요소 2개의 name을
        # username, password로 설정하고ㅗ
        # button type 'submit'을 실행

        # 전달되어온 POST  데이터에서 'username'과 'password'키의 값들을 사용
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # 만약 인증이 정상적으로 완료되었다면
        # 해당하는 username과 password에 일치하는 User개게가 존재할 경우
        if user is not None:
            login(request, user)
            return HttpResponse('Login Success')
        # 인증에 실패할 경우, 해당하는 username과 password에 일치하는 User개게가 존재하지 않을 경우
        else:
            return HttpResponse('Login Fail')
    # GET method로 요청이 왔을 경우,
    else:

        # member/login.html 템플릿을 render하여 return 하도록 함
        # return render(request, 'member/login.html')

        # html파일에서 POST요청을 보내기 위해
        # form을 정의하고, input 요소 2개의 name을
        # username, password로 설정하고ㅗ
        # button type 'submit'을 실행
        form = LoginForm()
        context = {
            'forms': form,
        }
        return render(request, 'member/login.html', context)
