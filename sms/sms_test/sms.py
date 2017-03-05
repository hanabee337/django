"""
1. .conf 폴더의 settings_local.json 파일 내용을 불러와
    json.loads()하여 config 변수에 할당(2017.02.24)
2. http://www.coolsms.co.kr/Python_SDK_EXAMPLE_Message에 있는 SMS(단문) 발송 구현해보기
"""
import json
import os
import sys

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(ROOT_DIR)

CONF_DIR = os.path.join(ROOT_DIR, '.conf')

config_content = open(os.path.join(CONF_DIR, 'settings_local.json')).read()
print(config_content)

config = json.loads(config_content)
print(config)

if __name__ == "__main__":
    # set api key, api secret
    api_key = config['sms']['API_KEY']
    api_secret = config['sms']['API_SECRET']

    # 4 params are mandatory, must be filled.
    params = dict()
    params['type'] = 'sms'  # Message type(sms, lms, mms, ata)
    params['to'] = config['sms']['receiver_num']  # Recipients Phone Number
    params['from'] = config['sms']['sender_num']  # Sender number
    params['text'] = 'Where are you?'  # Message to send

    cool = Message(api_key, api_secret)

    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID :%s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
