from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {

    }
    return render(request, 'common/index.html', context)

    # return HttpResponse()
