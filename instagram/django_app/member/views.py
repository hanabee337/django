"""
1. def login view를 마만들고
2. member app을 include 잉용해서
    /instagram/urls.py와 member/urls.py 모두 사용
3. login 뷰는 member/login URL과 연결되도록 member/urls.py 구현
4. login 뷰에서는 member/login.html 파일을 구현
5. settings.py에 TEMPLATES_DIR 변수를 할당하고 (os.path.join(BASE_DIR, 'templates'))
    TEMPLATES 설정의 DIRS에 추가
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from member.forms import LoginForm, SignupForm
from post.models import Post


def login_cf(request):
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

        # LoginForm을 사용
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 전달되어온 POST  데이터에서 'username'과 'password'키의 값들을 사용
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            # 만약 인증이 정상적으로 완료되었다면
            # 해당하는 username과 password에 일치하는 User개게가 존재할 경우
            if user is not None:
                login(request, user)
                # return HttpResponse('Login Success')
                return redirect('post:post_list')
            # 인증에 실패할 경우, 해당하는 username과 password에 일치하는 User개게가 존재하지 않을 경우
            else:
                # return HttpResponse('Login Fail')
                form.add_error(None, 'ID or PW Incorrect')
    # GET method로 요청이 왔을 경우,
    else:

        # member/login.html 템플릿을 render하여 return 하도록 함
        # return render(request, 'member/login.html')

        # html파일에서 POST요청을 보내기 위해
        # form을 정의하고, input 요소 2개의 name을
        # username, password로 설정하고
        # button type 'submit'을 실행

        # 빈 LoginForm 객체 생성
        form = LoginForm()

    context = {
        'forms': form,
    }
    return render(request, 'member/login.html', context)


def signup_fbv(request):
    """
    회원 가입 구현
    1. member/signup.html 파일 생성\
    2. SignupForm 클래스 구현
    3. 해당 Form을 사용해서 signup.html템플릿 구현
    4. POST요청을 받아 MyUser객체 생성
    5. 로그인 완료되면 post_list 뷰로 이동
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            login(request, user)
            return redirect('post:post_list')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }

    return render(request, 'member/signup.html', context)

@login_required
def profile(request):
    """
    1. button 1개 (로그아웃)이 존재하는 member/logout.html을 render해주는 view
    2. 메인의 우측 위 사람 모양 아이콘에 이 뷰로 오는 링크 연결
    """

    """
    자신의 게시물 수, 자신의 팔로워 수, 자신의 팔로우 수,
    context로 전달, 출력
    """
    # post_count = MyUser.objects.following.count()

    # if request.user.is_authenticated: -> @login_required로 대체한다.
    post_count = Post.objects.filter(author=request.user).count()
    follower_count = request.user.follower_set.count()
    following_count = request.user.following.count()
    print('{}, {}'.format(follower_count, following_count))
    context = {
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
    }

    return render(request, 'member/profile.html', context)
    # else:
    #     return redirect('member:login')


def logout_fbv(request):
    logout(request)
    return redirect('member:login')


def change_profile_image(request):
    """
    H/W:20170220
    해당 유저의 프로필 이미지를 바꾼다.
    0. 유저 모델에 img_profile 필드 추가, migrations
    1. change_profile_image.html 파일 작성
    2. ProfileImageorm 작성
    3. 해당 Form 템플릿에 렌더링
    4. request.method == 'POST' 일 때, request.FILES의 값을 이용해서
        request.user의 img_profile을 변결, 저장
    5. 처리 완료 후, member:profile로 이동
    6. progile.tml에서 user의 프로필 이미지를 img태그를 사용해서 보여줌.
        {{ MEDIA_URL }}을 사용함.
    """