from django.shortcuts import render, redirect

from .models import Post, Comment

"""
Post List를 보여주는 화면을 구성
1. View에 post_list 함수 작성
2. Template에 post_list.hrml 파일 작성
3. view에서 post_list.html을 render한 결과를 리턴하도록 함
4. instagram/urls.py에 post/urls.py를 연결시킴(app_naem을 post) : name-spacing
5. '/post/'로 접속했을 때, post_list view에 연결되도록 post/urls.py에 내용을 작성
6. 전체 post를 가져오는 쿼리셋을 context로 넘기도록 post_list 뷰에 구현
7. post_list.html에서 {% for %}태그를 사용해 post_list의 내용을 순회하며 표현
"""


def post_list(request):
    # return HttpResponse('post_list view')
    post = Post.objects.all()
    context = {
        'post_list': post
    }
    return render(request, 'post/post_list.html', context)


"""
Post detail(하나의 Post에 대한 상세화면)
1. View애  post_detail 함수 작성
2. 위의 2~4와 같음.
5. 'post/<숫자>/'로 접속했을 때, post_detail view에
    연결되도록 post/urls.py에 내용 작성
6. url인자로 전달받은 post_id에 해당하는 Post 객체를
    context에 넘겨 post_detail화면을 구성

post Detail 댓글작성기능 추가
1. request.method 에 따라 로직이 분리되도록 if/else 추가
2. request.method = POST 일 경우, request.POST에서 'content' 키의 값을 가져옴
3. 현재 로그인한 유저는 request.uuser로 가져오묘, Post의 id 값은 post_idㅇ;ㄴ지러 잔딜더되므로 두 내용을 사용
4. 위 내용물과 content를 사용해서 Comment 객체를 생성 및 저장
"""


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'post_detail': post
    }
    return render(request, 'post/post_detail.html', context)


def comment_add(request, post_id):
    print('comment_add')

    if request.method == 'POST':
        print('POST')
        content = request.POST['content']
        user = request.user
        post = Post.objects.get(id=post_id)

        Comment.objects.create(
            author=user,
            post=post,
            content=content
        )
        return redirect('post:post_detail', post_id=post_id)
    else:
        print('NO POST')