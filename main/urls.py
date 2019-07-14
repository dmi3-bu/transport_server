from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/main')),
    path('main', views.main),
    path('login', views.login_view),
    path('register', views.register),
    path('logout', views.logout_view),
    path('qr', views.qr_view),
    path('admin-panel', views.genQR, name='admin-panel'),
    path('api/login', views.api_login),
    # path('api/beacons', views.beacons_index)
]
