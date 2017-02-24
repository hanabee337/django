from django.http import HttpResponse
from django.shortcuts import render

from sms_test.forms import SMSForm


def index(request):
    if request.method == 'POST':
        form = SMSForm(request.POST)
        if form.is_valid():
            numbers = form.cleaned_data['recipient_numbers']
            content = form.cleaned_data['content']
            # for number in numbers:
            #     pass
            return HttpResponse(', '.join(numbers))
    else:
        form = SMSForm(
            initial={
                # 'recipient_numbers': '010-3265-6734, 01032656734, 01023412, 293849323232, 02394090930',
                'recipient_numbers': '010-3265-6734, 01032656734',
            }
        )

    context = {
        'form': form,
    }
    return render(request, 'common/index.html', context)