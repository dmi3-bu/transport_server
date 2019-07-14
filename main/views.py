from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.core.files import File
from main.models import Ticket
from .forms import UserRegisterForm, UserLoginForm, SearchForm, GenQRForm
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
from urllib.parse import urlencode
import qrcode
from django.conf import settings
from io import BytesIO

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





@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'status': 'Ошибка: Введите пароль и логин'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'status': 'Ошибка: неправильные логин или пароль'},
                        status=HTTP_404_NOT_FOUND)
    return Response({'status': 'success'},
                    status=HTTP_200_OK)


@login_required
def genQR(request):
    if request.method == "POST":
        form = GenQRForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['passport'] is not '':
                user = User.objects.get(passport=form.cleaned_data['passport'])
                ticket = Ticket(user_id=user)
                code_qr = str(ticket.id)

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )

                qr.add_data(code_qr)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                name_img = "qr-" + code_qr + '.png'
                img_path = settings.MEDIA_ROOT + '/' + name_img
                blob = BytesIO()
                img.save(blob)
                ticket.image.save(name_img, File(blob), save=False)
                ticket.save()

                return redirect('/qr', {'ticket': ticket})
            else:
                if form.cleaned_data['ticket_id'] is not '':
                    t = Ticket.objects.get(id=form.cleaned_data['ticket_id'])
                    user = User.objects.get(id=t.user_id)
                    t.delete()
                    tickets = Ticket.objects.filter(user_id=user.id)
                    return render(request, 'info_admin.html', {'tickets': tickets, 'finded_user': user})

    else:
        form = GenQRForm()
    return render(request, 'info_admin.html', {'form': form, 'passport': request.GET['passport']})


@login_required
def main(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['passport'] is not '':
                finded_user = User.objects.get(passport=form.cleaned_data['passport'])
                tickets = Ticket.objects.filter(user_id=finded_user.id)
            if form.cleaned_data['ticket_id'] is not '':
                ticket = Ticket.objects.get(id=form.cleaned_data['ticket_id'])
                finded_user = User.objects.get(id=ticket.user_id)
                tickets = Ticket.objects.filter(user_id=finded_user.id)
            base_url = reverse('admin-panel')
            query_string = urlencode({'passport': finded_user.passport})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)  # 4
    else:
        form = SearchForm()
    return render(request, 'main.html', {'form': form})


def qr_view(request):
    return render(request, 'qr.html')
