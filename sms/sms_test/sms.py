"""
1. .conf 폴더의 settings_local.json 파일 내용을 불러와
    json.loads()하여 config 변수에 할당
"""
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(ROOT_DIR)

CONF_DIR = os.path.join(ROOT_DIR, '.conf')

config_content = open(os.path.join(CONF_DIR, 'settings_local.json')).read()
print(config_content)

config = json.loads(config_content)
print(config)
