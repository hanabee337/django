from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login_fbv(request):
    return render(request, 'member/login.html')
