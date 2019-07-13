from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def login(request):
    context = {
        # 'murren': murren,
        # 'already_follow': already_follow
    }
    return render(request, 'login.html', {})


def register(request):
    return render(request, 'register.html', {})


@login_required
def main(request):
    context = {
        # 'murren': murren,
        # 'already_follow': already_follow
    }
    return render(request, 'main.html', context)
    pass


def logout(request):
    pass