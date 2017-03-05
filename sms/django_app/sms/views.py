import json
import os
import sys

from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from sms.forms import SMSForm


def send_sms(number, content):
    config_content = Path(__file__).parents[2].joinpath('.conf', 'settings_local.json').open().read()
    config = json.loads(config_content)
    print('config: {}'.format(config))

    # if __name__ == "__main__":
    # set api key, api secret
    api_key = config['sms']['API_KEY']
    api_secret = config['sms']['API_SECRET']

    # 4 params are mandatory, must be filled.
    params = dict()
    params['type'] = 'sms'  # Message type(sms, lms, mms, ata)
    params['to'] = number  # Recipients Phone Number
    params['from'] = config['sms']['sender_num']  # Sender number
    params['text'] = content  # Message to send

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

    # sys.exit()


def index(request):
    if request.method == 'POST':
        print(request.POST)
        print('recipient_numbers: {}'.format(request.POST['recipient_numbers']))
        print('content: {}'.format(request.POST['content']))
        form = SMSForm(request.POST)

        if form.is_valid():
            numbers = form.cleaned_data['recipient_numbers']
            content = form.cleaned_data['content']
            for number in numbers:
                # pass
                send_sms(number, content)

            return HttpResponse(', '.join(numbers))
    else:
        form = SMSForm(
            initial={
                'recipient_numbers': '010-1234-5678, 01012345678, 01023412, 293849323232, 02394090930'
            }
        )

    context = {
        'form': form,
    }
    return render(request, 'common/index.html', context)
