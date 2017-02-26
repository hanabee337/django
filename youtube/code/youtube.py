"""
실습 - 2017.02.21
1. .conf폴더의 settings_local.json을 읽어온다
2. 해당 내용을 json.loads()를 이용해 str -> dict형태로 변환
3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
5. 이후 내부에 있는 검색결과를 적절히 루프하며 print해주기
"""
import json
import os
from pprint import pprint

import requests
from dateutil.parser import parse

# 1. .conf폴더의 settings_local.json을 읽어온다
# .conf폴더까지의 PATH를 특정화해서 변수에 할당
# -> print(특정화한 PATH변수) 를 하면
#       .....(경로)/.conf/settings_local.json
#            이 출력되어야 함
# 파이썬에서 파일 읽는 내장함수를 사용해서 결과를 다시 변수에 할당
# 현재 파일 (youtube/code/youtube.py)

current_path = os.path.abspath(__file__)
print(current_path)

# 현재 파일에서 한 단계 부모 디렉토리 (youtube/code)
# code디렉토리 보다 한 단계 위, 즉 현재 파이참 프로젝트 루트 폴더 (youtube)
root_path = os.path.dirname(os.path.dirname(current_path))
print(root_path)

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
print('config: %s' % config)

youtube_api_key = config['youtube']['API_KEY']
print(youtube_api_key)

# 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
# 이렇게 Parameter와 URL을 분리합니다
params = {
    'key': youtube_api_key,
    'part': 'snippet',
    'q': '송지효',
    'type': 'video',
    'maxResults': 5,
}
r = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
print(r)
print(r.json())

content = r.text
print(content)


# 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
result_dict = json.loads(content)
pprint(result_dict)

# 5. 이후 내부에 있는 검색결과를 적절히 루프하며 print해주기
items = result_dict['items']

for item, index in enumerate(items):
    title = item['snippet']['title']
    published_date_str = item['snippet']['publishedAt']
    description = item['snippet']['description']
    youtube_id = item['id']['videoId']
    thumbnail_url = item['snippet']['thumbnails']['high']['url']

    # pip install python-dateutil
    published_date = parse(published_date_str)
