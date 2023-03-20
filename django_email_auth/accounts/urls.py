from django.urls import path, include
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('register/', register_attempt, name="register_atempt"),
    path('login/', login_attempt, name="login_attempt"),
    path('token/', token_send, name="token_send"),
    path('success/', success, name="success"),
]
