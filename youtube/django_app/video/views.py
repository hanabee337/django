"""
2017.02.21
- search view의 동작 변경
1. keyword로 전달받은 검색어를 이용한 결과를 데이터베이스에 저장하는 부분 삭제
2. 결과를 적절히 가공하거나 그대로 템플릿으로 전달
3. 템플릿에서는 해당 결과를 데이터베이스를 거치지 않고 바로 출력
"""
from django.contrib.auth.decorators import login_required

from video.models import Video

"""
2017.02.21
- Next, Prev버튼 추가
1. Youtube Search API에 요청을 보낸 후, 결과에
    1-2. nextPageToken만 올 경우에는 첫 번째 페이지
    1-3. 둘다 올 경우에는 중간 어딘가
    1-4. prevPageToken만 올 경우에는 마지막 페이지 임을 알 수 있음
2. 템플릿에 nextPageToken, prevPageToken을 전달해서
    해당 token(next또는 prev)값이 있을 경우에 따라
    각각 '다음' 또는 '이전' 버튼을 만들어 줌
"""
import json
import os

import requests
from dateutil.parser import parse
from django.shortcuts import render, redirect


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
    # print('request.path_info: %s' % request.path_info)
    print('request.get_full_path: %s' % request.get_full_path())

    videos = []
    context = {
        'videos': videos,
    }

    # print(request.GET)

    page_token = request.GET.get('page_token')

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

        # 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
        # 이렇게 Parameter와 URL을 분리합니다
        params = {
            'part': 'snippet',
            'key': youtube_id,
            'q': keyword,
            'type': 'video',
            'maxResults': 5
        }
        # 페이지 토큰값이 전달되었을 때만 params에 해당 내용을 추가해서 요청
        if page_token:
            params['pageToken'] = page_token

        r_dict = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        # print(r_dict)
        # print(r_dict.text)
        # 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
        content = json.loads(r_dict.text)
        # print(content)

        # 검색결과에서 이전/다음 토큰, 전체 결과 개수를 가져와
        # 템플릿에 전달할 context객체에 할당한다.
        # 그런데, .get으로 한 이유는 만약 찾는 게 없으면 None으로 반환되니..
        # template에서 if 문으로 처리 할 수가 있다.
        next_page_token = content.get('nextPageToken')
        # print('next_page_token: %s' % next_page_token)
        prev_page_token = content.get('prevPageToken')
        # print('prev_page_token: %s' % prev_page_token)
        total_results = content['pageInfo'].get('totalResults')
        context['next_page_token'] = next_page_token
        context['prev_page_token'] = prev_page_token
        context['total_results'] = total_results
        context['keyword'] = keyword

        # videos = get_videos(content)

        items = content['items']
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

    # context = {
    #     'videos': videos,
    # }
    return render(request, 'video/search.html', context)


@login_required
def bookmark_add(request):
    print('bookmark_add')

    if request.method == 'POST':
        title = request.POST['title']
        youtube_id = request.POST['youtube_id']
        description = request.POST['description']
        published_date_str = request.POST['published_date']
        print(published_date_str)
        published_date = parse(published_date_str)
        print(published_date)
        prev_path = request.POST['path']

        defaults = {
            'title': title,
            'description': description,
            'published_date': published_date
        }

        # video = Video.objects.get_or_create
        # 이렇게 하면, 아래와 같은 에러가 발생함.
        # 꼭, video, _ = Video.objects.get_or_create 이렇게 해야 함.why(?)
        # TypeError at /video/bookmark/add/
        # int() argument must be a string,
        # a bytes-like object or a number, not 'Video'
        #         <  get_or_create(defaults=None, **kwargs)  >
        # Returns a tuple of (object, created), where object is the retrieved
        # or created object and created is a boolean specifying whether a new
        # object was created.
        video, _ = Video.objects.get_or_create(
            defaults=defaults,
            youtube_id=youtube_id
        )
        request.user.bookmark_videos.add(video)

        # return redirect('video:search')
        # redirect는 POST 요청을 보내는 것이 불가능하다.
        # 그렇기 때문에, redirect로 가야되는 이전 page에 대한 정보는
        # GET parameter에 모든 걸 넣어놔야 한다.
        # 그 정보는 request.get_full_path에 있다.
        # 이전에 요청했던 URL정보를 가져옴(GET parameter포함)
        # POST 요청을 받았을 때는 기존에 어디였는지를
        # template에서 이전 페이지에 대한 path를 보내주어야 한다.
        # 그럼, template에선 이전 페이지에 대한 path를 어떻게 아느냐?
        # get_full_path를 사용해서 알 수가 있다.
        return redirect(prev_path)
