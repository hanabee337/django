from django.http import HttpResponse
from django.shortcuts import render

from sms.forms import SMSForm


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
                pass
                # send_sms(number, content)

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
