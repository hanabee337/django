from django.db import models

from member.models import MyUser
from .post import Post

__all__ = (
    'Comment',
)


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{}]\'s Comment[{}], Author[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )
