
import json
import os

import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
ROOT_DIR = os.path.dirname(BASE_DIR)
CONF_DIR = os.path.join(ROOT_DIR, '.conf')

# Load config file
config = json.loads(open(os.path.join(CONF_DIR, 'settings_local.json')).read())
print(config)


if __name__ == "__main__":
    api_key = config['sms']['API_KEY']
    api_secret = config['sms']['API_SECRET']

    params = dict()
    params['type'] = 'sms'
    params['to'] = '01032656734'
    params['from'] = config['sms']['sender_num']
    params['text'] = 'WHO are you?'

    cool = Message(api_key=api_key, api_secret=api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print('Error List: %s' % response['error_list'])

    except CoolsmsException as e:
        print("Error Code: %s" % e.code)
        print("Error Message: %s" % e.msg)

    sys.exit()