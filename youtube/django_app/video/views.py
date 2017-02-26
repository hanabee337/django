"""
search view의 동작 변경
1. keyword로 전달받은 검색어를 이용한 결과를 데이터베이스에 저장하는 부분 삭제
2. 결과를 적절히 가공하거나 그대로 템플릿으로 전달
3. 템플릿에서는 해당 결과를 데이터베이스를 거치지 않고 바로 출력
"""

import json
import os

import requests
from dateutil.parser import parse
from django.shortcuts import render


def get_config():
    current_path = os.path.abspath(__file__)
    # print(current_path)

    # 현재 파일에서 두 단계 부모 디렉토리
    base_path = os.path.dirname(os.path.dirname(current_path))
    # print(base_path)

    root_path = os.path.dirname(base_path)

    # 루트 폴더의 바로 아래 .conf폴더 (youtube/.conf)
    conf_path = os.path.join(root_path, '.conf')
    # print(conf_path)

    # .conf폴더 내부의 settings_local.json파일
    file_path = os.path.join(conf_path, 'settings_local.json')
    content = json.loads(open(os.path.join(conf_path, 'settings_local.json')).read())
    # print(content['youtube']['API_KEY'])

    # 파일을 열고 읽고 닫아준다
    # f = open(path_file_settings_local, 'r')
    # config_str = f.read()
    # f.close()
    with open(file_path, 'r') as f:
        config_str = f.read()
    # print(config_str)
    # print(type(config_str))

    # 2. 해당 내용을 json.loads()를 이용해 str -> dict형태로 변환
    # 해당내용 -> 1번에서 최종 결과
    config = json.loads(config_str)
    # print('type(config) : %s' % type(config))
    # print(config)

    youtube_api_key = config['youtube']['API_KEY']
    # print(youtube_api_key)

    return youtube_api_key


def get_videos(content):
    items = content['items']
    videos = []

    for item in items:
        # 실제로 사용될 데이터
        title = item['snippet']['title']
        published_date_str = item['snippet']['publishedAt']
        description = item['snippet']['description']
        youtube_id = item['id']['videoId']
        thumbnail_url = item['snippet']['thumbnails']['high']['url']

        # pip install python-dateutil
        published_date = parse(published_date_str)

        # 현재 item을 dict으로 정의
        video = {
            'title': title,
            'description': description,
            'youtube_id': youtube_id,
            'publishedAt': published_date,
            'thumbnail_url': thumbnail_url,
        }
        videos.append(video)

        # 단순히 Video.objects.create을 하면 검색할 때 마다
        # DB에 중복되게 저장이 된다. 이를 방지하기 위해
        # youtube_id를 unique하게 설정을 하였음.
        # 그래서, create 대신,
        # get_or_create(있으면 가져오거나, 없으면 새로 만들어 save함)를 사용하였고,
        # 그러나, title이나 description이 같은 것들은 걸러내지 못함.
        # 그래서, get_or_create argumnet에 defaults를 추가함.
        # get을 했는데, 있으면 object를 가져오고,
        # 없으면, new object를 create하는데, 이때 defaults 로 설정한
        # arguments들을 사용함.
        # get_or_create commit=false로 googling.
        # defaults = {
        #     'title': title,
        #     'description': description,
        #     'published_date': published_date
        # }
        # get_or_created를 안쓰면, try, except로 하는 방법이 있다.
        # 그러나, 코드가 길어짐.
        # video, video_created = Video.objects.get_or_create(
        #     youtube_id=youtube_id,
        #     defaults=defaults
        # )
        # if not video_created:
        #     print('youtube id: %s ' % youtube_id)
        #     print('title: %s' % title)
    # videos = Video.objects.all()

    return videos


def search(request):
    videos = []

    print(request.GET)
    keyword = request.GET.get('keyword', '').strip()
    # request.GET['keyword']로 할 수 도 있지만,
    # 만약, keyword가 없는 경우(keyword에 해당하는 key값이 없는 경우,
    # 에러가 발생한다.
    # 이를 방지하기 위해 .get을 사용한다.
    # 또한, request.GET.get('keyword')했는데,
    # 어떤 key값으로 get을 했는데, value가 없으면 None 객체가 오게 됨.
    # 그리고, value가 blank인 경우 두 가지를 대비하기 위해,
    # request.GET.get('keyword', '')로 설정

    # GET parameters의 keyword값이 왔을 떄에만 검사결과에 내용이 추가됨.
    # request.POST로 하면, url이 바뀌지 않는다.
    # request.POST를 할 필요가 없는,
    # 즉, url 주소를 공유할 필요가 있는 경우는
    # request.GET으로 설정하는데, url뒤에 더 추가되는 형태로 바뀌게 된다.
    # request.GET으로 하면, dict 형태로 나오는데,
    if keyword != '':
        youtube_id = get_config()

        params = {
            'part': 'snippet',
            'key': youtube_id,
            'q': keyword,
            'type': 'video',
            'maxResults': 10
        }
        r_dict = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        # print(r_dict)
        # print(r_dict.text)
        content = json.loads(r_dict.text)
        # print(content)
        videos = get_videos(content)

    context = {
        'videos': videos,
    }
    return render(request, 'video/search.html', context)
