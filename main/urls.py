from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/main')),
    path('main', views.main),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
]
