from django.http import HttpResponse
from django.shortcuts import render

from sms.forms import SMSForm


def index(request):
    if request.method == 'POST':
        print(request.POST)
        print('recipient_numbers: {}'.format(request.POST['recipient_numbers']))
        print('content: {}'.format(request.POST['content']))
        forms = SMSForm(request.POST)

        if forms.is_valid():
            numbers = forms.cleaned_data['recipient_numbers']
            return HttpResponse(','.join(numbers))
    else:
        forms = SMSForm(
            initial={
                'recipient_numbers': '010-1234-5678, 01012345678, 01023412, 293849323232, 02394090930'
            }
        )

    context = {
        'forms': forms,
    }
    return render(request, 'common/index.html', context)
