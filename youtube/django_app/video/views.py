"""
20170221 - H/W
1. video app을 생성하고
2. 유튜브 영상의 정보를 저장할 수 있는 Model 구현, Migration
3. POST 요청을 받으면 요청에서 온 키워드로 유투브를 검색 후, 결과를 DB에 저장하는 View 구현
    방금 작성한 code/youtube.py파일의 내용을 하나의 함수로 구현
    - 저장 후, 해당 결과 Query를 리턴해서 템플릿에서 보여주도록 구현
    - 또는 저장된 모든 결과를 리턴해서 템플릿에서 보여주기
    - 이미 저장된 영상정보는 저장하지 않고 넘어가기
4. 위 View를 나타낼 수 있는 Template 구현
5. View와 Template연결
6. 실행해 보기
"""
import json
import os

import requests
from django.shortcuts import render

from .models import VideoModel


def get_config():
    current_path = os.path.dirname(__file__)
    print(current_path)
    base_path = os.path.dirname(current_path)
    print(base_path)
    root_path = os.path.dirname(base_path)
    print(root_path)

    conf_path = os.path.join(root_path, '.conf')
    print(conf_path)

    f = open(os.path.join(conf_path, 'settings_local.json'))
    content = f.read()
    f.close()
    config = json.loads(content)

    return config


def get_requests_from_youtube(keyword, key):
    params = {
        'part': 'snippet',
        'q': keyword,
        'key': key,
        'type': 'video',
        'maxResults': 5,
    }

    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
    print(r.text)
    result = r.text

    result_dict = json.loads(result)
    return result_dict


def search(request):

    videos = []

    if request.method == 'POST':
        keyword = request.POST['keyword']
        print(keyword)

        key = get_config()['youtube']['API_KEY']
        print(key)

        result_dict = get_requests_from_youtube(keyword, key)

        print(result_dict['items'])
        items = result_dict['items']
        for item in items:
            title = item['snippet']['title']
            description = item['snippet']['description']
            published_date = item['snippet']['publishedAt']
            youtube_id = item['id']['videoId']

            defaults = {
                'title': title,
                'description': description,
                'published_date': published_date,
            }
            # 그냥 VideoModel.objects.create하면 Model에서 설정해준 unique 속성 때문에 integrity error가 발생한다.
            # unique로 설정한 이유는 동일한 video를 걸러내기 위함이다.
            VideoModel.objects.get_or_create(
                youtube_id=youtube_id,
                defaults=defaults
            )

        videos = VideoModel.objects.all()

    context = {
        'videos': videos,
    }
    return render(request, 'video/search.html', context)
