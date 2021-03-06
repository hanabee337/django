from django.shortcuts import render, redirect

from post.forms import CommentForm, PostForm
from post.models import Post

__all__ = (
    'post_list',
    'post_detail',
    'post_like_toggle',
    'post_add',
    'post_delete',
)

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
    # post = Post.objects.all()
    post = Post.objects.filter(is_visible=True)
    # post = Post.visible.all()
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
    # 인자로 전달된 post_id와 일치하는 id를 가진 Post객체 하나만 조회
    post = Post.objects.get(id=post_id)
    # Comment를 생성할 Form객체를 생성, 할당
    comment_form = CommentForm()
    # like_form = LikeForm()

    context = {
        'post_detail': post,
        'comment_form': comment_form,
        # 'like_form': like_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_add(request):
    print('post_add')

    def create_post_comment(file, comment_content):
        post = Post(
            author=request.user,
            photo=file,
        )
        post.save()

        if comment_content != '':
            post.add_comment(user=request.user, content=comment_content)
            # post.comment_set.create(
            #     author=request.user,
            #     content=comment_content
            # )

    """
    1. template : post_add.html
    2. view : def post_add
    3. url : /post/add/
    4. form : post.form.PostForm
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print('post_add method:POST')
        if form.is_valid():
            comment_content = form.cleaned_data.get('content', '').strip()
            files = request.FILES.getlist('photo')

            for file in files:
                create_post_comment(file, comment_content)

            """
            2017.02.17
            1. Post 모델에서 content 필드를 없애고 Db migration
            2. post_add view의 동작을 변경 : 입력받은 content는 새 comment 객체를 생성하도록)
            """

            return redirect('post:post_list')
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'post/post_add.html', context)


def post_delete(request, post_id, db_delete=False):
    print('post_delete')

    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if post.author.id == request.user.id:
            if db_delete:
                post.delete()
            else:
                post.is_visible = False
                post.save()

        return redirect('post:post_list')


def post_like_toggle(request, post_id):
    """
    1. post_detail.html에 form을 하나 더 생성
    2. 요청 view(url)가 post_like가 되도록 함
    3. 요청을 받은 후, 적절히 PostLike 처리
    4. redirect
    """
    print('post_like')

    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.toggle_like(user=request.user)
        return redirect('post:post_list')
