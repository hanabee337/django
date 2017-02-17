from django.shortcuts import redirect

from post.forms import CommentForm
from post.models import Post, Comment

__all__ = (
    'comment_add',
    'comment_delete',
)


def comment_add(request, post_id):
    print('comment_add')

    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():
            print('POST')
            content = form.cleaned_data['content']
            # HttpRequest에는 항상 User정보가 전달된다.
            user = request.user
            # url 인자로 전달된 post_id 값을 사용
            post = Post.objects.get(id=post_id)

            # post의 메서드를 사용해서 Comment객체 생성
            post.add_comment(user, content)
            # Comment.objects.create(
            #     author=user,
            #     post=post,
            #     content=content
            # )
        # 다시 해당하는 post_detail로 redirect
        return redirect('post:post_list')

    else:
        print('NO POST')


def comment_delete(request, post_id, comment_id):
    """
    1. Post_detail.html의 Comment 표현 loop내부에 form을 생성
    2. 요청 view(url)가 comment_delete가 되도록 함.
    3. 요청을 받은 후, 적절히 삭제 처리
    4. redirect
    """
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        if comment.author.id == request.user.id:
            comment.delete()
        return redirect('post:post_detail', post_id=post_id)
        # return redirect('post:post_list', post_id=post_id)