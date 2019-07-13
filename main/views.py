from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import get_user_model, authenticate, login
User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/main')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    logout(request)


def register(request):
    if request.method == 'POST':
        if request.POST['password'] != request.POST['password2']:
            return render(request, 'register.html', {'form': UserRegisterForm()})
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(**form.cleaned_data)
            client_group = Group.objects.get(name='Client')
            user.groups.set([client_group])
            user.save()
            login(request, user)
            return redirect('/main')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def main(request):
    context = {
        # 'murren': murren,
        # 'already_follow': already_follow
    }
    return render(request, 'main.html', context)
    pass

