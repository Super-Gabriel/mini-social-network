from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('logIn/', redirectToLogIn, name='redirectToLogIn'),
    path('createAc/', redirectToCreateAc, name='redirectToCreateAc'),
    path('superLogIn/', redirectToLogInSuperUsr, name='redirectToLogInSuperUsr')
]