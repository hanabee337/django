from django.db import models

# Create your models here.
"""
20170221 - H/W
1. video app을 생성하고
2. 유튜브 영상의 정보를 저장할 수 있는 Model 구현, Migration
3. POST 요청을 받으면 요청에서 온 키워드로 유투브를 검색 후, 결과를 DB에 저장하는 View 구현
4. 위 View를 나타낼 수 있는 Template 구현
5. View와 Template연결
6. 실행해 보기
"""


class VideoModel(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    youtube_id = models.CharField(unique=True, max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
