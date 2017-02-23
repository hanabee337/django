# Create your views here.
from django.shortcuts import render


def search(request):
    context = {

    }
    return render(request, 'video/search.html', context)
