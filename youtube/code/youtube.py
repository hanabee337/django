"""
20170221 15:00 - youtube api 실습
1. .conf 폴더의 settings_local.json을 읽어온다
    파이썬에서 파일 읽는 내장함수를 사용해서 결과를 다시 변수에 할당.
2. 해당 내용을 json.loads()를 이용해 str-> dict 형태로 변환
3. requests 라이브러리를 이용(pip install requests), GET 요청으로 데이터를 받아온 후,
4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
5. 이후 내부에 있는 검색 결과를 적절히 루프하면 print 해주기
"""
import json
import os
from pprint import pprint

import requests

# 현재 파일(youtube/code/youtube.py)
current_file_path = os.path.abspath(__file__)

# 부모 디렉토리
go_to_parent_path = os.path.dirname(current_file_path)

# 할아버지 디렉토리
go_to_grand_path = os.path.dirname(go_to_parent_path)

# 할아버지 디렉토리(루트 디렉토리)의 바로 아래, .conf 폴더 (youtube/.conf)
go_to_parent_path = os.path.join(go_to_grand_path, '.conf')

# .conf 폴더 내부의 settings_local.json
go_to_child_path_or_file = os.path.join(go_to_parent_path, '.settings_local.json')

print(current_file_path)
print(go_to_grand_path)
print(go_to_child_path_or_file)

# 1. .conf 폴더의 settings_local.json을 읽어온다
f = open(os.path.join(go_to_parent_path, 'settings_local.json'), 'r')
content = f.read()
f.close()

# with open(os.path.join(go_to_parent_path, 'r')) as f:
# content = f.read()

# 2. 해당 내용을 json.loads()를 이용해 str-> dict 형태로 변환
config = json.loads(content)
print(config)
youtube_api_key = config['youtube']['API_KEY']
print(youtube_api_key)

# 3. requests 라이브러리를 이용(pip install requests), GET 요청으로 데이터를 받아온 후,
param = {
    'key': config['youtube']['API_KEY'],
    'part': 'snippet',
    'q': '민아',
    'maxResults': 30,
    'type': 'video',
}

r = requests.get('https://www.googleapis.com/youtube/v3/search', params=param)
print(r.url)
print(r.json())
result = r.text

# 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
result_dict = json.loads(result)

# 5. 이후 내부에 있는 검색 결과를 적절히 루프하면 print 해주기
pprint(json.loads(result))

kind = result_dict['kind']
etag = result_dict['etag']
item = result_dict['items']
next_page_token = result_dict['nextPageToken']
region_code = result_dict['regionCode']
page_info = result_dict['pageInfo']

print('kind %s' % kind)
print('etag %s' % etag)
print('next_page_token %s' % next_page_token)
print('region_code %s' % region_code)
print('page_info %s' % page_info)

items = result_dict['items']
for index,item in enumerate(items):
    title = item['snippet']['title']
    published_date = item['snippet']['publishedAt']
    print(title, published_date)


