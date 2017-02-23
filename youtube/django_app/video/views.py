# Create your views here.
import json
import os

import requests
from dateutil.parser import parse
from django.shortcuts import render


def get_config():
    current_path = os.path.abspath(__file__)
    print(current_path)

    # 현재 파일에서 두 단계 부모 디렉토리
    base_path = os.path.dirname(os.path.dirname(current_path))
    print(base_path)

    root_path = os.path.dirname(base_path)

    # 루트 폴더의 바로 아래 .conf폴더 (youtube/.conf)
    conf_path = os.path.join(root_path, '.conf')
    print(conf_path)

    # .conf폴더 내부의 settings_local.json파일
    file_path = os.path.join(conf_path, 'settings_local.json')
    content = json.loads(open(os.path.join(conf_path, 'settings_local.json')).read())
    print(content['youtube']['API_KEY'])

    # 파일을 열고 읽고 닫아준다
    # f = open(path_file_settings_local, 'r')
    # config_str = f.read()
    # f.close()
    with open(file_path, 'r') as f:
        config_str = f.read()
    print(config_str)
    print(type(config_str))

    # 2. 해당 내용을 json.loads()를 이용해 str -> dict형태로 변환
    # 해당내용 -> 1번에서 최종 결과
    config = json.loads(config_str)
    print('type(config) : %s' % type(config))
    print(config)

    youtube_api_key = config['youtube']['API_KEY']
    print(youtube_api_key)

    return youtube_api_key


def get_videos(content):
    items = content['items']
    videos = []

    for item in items:
        title = item['snippet']['title']
        published_date_str = item['snippet']['publishedAt']
        description = item['snippet']['description']
        youtube_id = item['id']['videoId']
        thumbnail_url = item['snippet']['thumbnails']['high']['url']

        # pip install python-dateutil
        published_date = parse(published_date_str)

        video = {
            'title': title,
            'description': description,
            'youtube_id': youtube_id,
            'publishedAt': published_date,
            'thumbnail_url': thumbnail_url,
        }
        videos.append(video)

    return videos


def search(request):
    videos = []

    if request.method == 'POST':
        keyword = request.POST['keyword']
        youtube_id = get_config()

        params = {
            'part': 'snippet',
            'key': youtube_id,
            'q': keyword,
            'type': 'video',
            'maxResults': 10
        }
        r_dict = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        print(r_dict)
        print(r_dict.text)
        content = json.loads(r_dict.text)
        print(content)
        videos = get_videos(content)

    context = {
        'videos': videos,
    }
    return render(request, 'video/search.html', context)
