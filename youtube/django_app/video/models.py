from django.db import models


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    published_date = models.DateTimeField()
    youtube_id = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.title

"""
2017.02.22
- 북마크 기능을 만든다
class Video에서 MTM을 쓰면
같은 영상에 대해, 같은 정보에 대해 여러 개가 생김. 유저만 다르고.
그래서, Video에 대해서, User에서 연결을 시켜주는 것이 깔끔해 보임
"""


