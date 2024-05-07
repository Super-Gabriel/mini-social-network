from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def redirectToLogIn(request):
    return redirect('inicioSesion')

def redirectToCreateAc(request):
    return redirect('crearCta')

def redirectToLogInSuperUsr(request):
    return redirect('logIn_adm')