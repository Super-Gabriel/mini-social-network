from django.urls import path
from .views import *
 
urlpatterns = [
    path('prueba/', prueba, name="prueba"),
    path('', inicioSesion, name='inicioSesion'),
    path('perfil/', perfil, name="perfil"),
    path('succes/<str:correo>/', perfil_success, name='perfil_success'),
    path('estado/', actualizar, name="actualizarEdo"),
    path('logOut/<str:correo>', logOut, name="logOut"),
    path('friends/<str:correo>', friends, name="friends"),
    path('chats/<str:correo>', chats, name='chats'),
    path('inbox/<str:correo>/<str:correo1>', inbox, name="inbox"),
    path('editar/<str:correo>', edit, name='edit')
]