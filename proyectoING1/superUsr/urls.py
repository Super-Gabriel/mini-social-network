from django.urls import path
from .views import *

urlpatterns = [
    path('', logIn_adm, name='logIn_adm'),
    path('success/<str:correo>', success_adm, name='success_adm'),
    path('logOut/<str:correo>', logOut_adm, name='logOut_adm')
]