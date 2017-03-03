from django.shortcuts import redirect, render


def index(request):
    # return redirect('member:login')
    return render(request, 'common/index.html')