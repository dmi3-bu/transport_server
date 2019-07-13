from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/main')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')

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


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Ошибка: Введите пароль и логин'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Ошибка: неправильные логин или пароль '},
                        status=HTTP_404_NOT_FOUND)
    return Response({'status': 'success'},
                    status=HTTP_200_OK)
