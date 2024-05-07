from django.urls import path
from .views import *

urlpatterns = [
    path('',crearCta, name="crearCta"),
    path('addResult/',agregarCta, name="agregarCta"),
    path('home/', redirectToHome, name="redirectToHome")
]