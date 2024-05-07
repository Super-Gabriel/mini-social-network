from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.models import *

# Create your views here.
def crearCta(request):
    return render(request, 'crearCta.html')

def agregarCta(request):
    result = HttpResponse(f'default')

    nom = request.POST.get('nombre')
    corr = request.POST.get('correo')
    cont = request.POST.get('contra')
    cont2 = request.POST.get('contraValid')
    fecha = request.POST.get('fechaNac')
    genero = request.POST.get('genero')

    datos = [nom,corr,cont,cont2,fecha,genero]

    # para verificar que no sean nulos
    if all(x is not "" for x in datos):

        #para ver que el correo no esté en la base de datos
        try:
            validarCorreo = UsuariosDB.objects.get(correo=corr)
            return render(request, 'errorCrearCta.html',{'reason': "correo ya en uso :c"})
        except:
            True

        #para ver que las contras coincidan
        if cont == cont2:
            try:
                newUser = UsuariosDB(nombre=nom,correo=corr,contra=cont,fecha=fecha,genero=genero)
                newUser.save()
                result = render(request,'succes.html')
            except:
                result = render(request,'errorCrearCta.html',{'reason': "algo salió mal en la base de datos"})

        else:
            result = render(request,'errorCrearCta.html', {'reason':"las contraseñas no coinciden :c"})

    else:
        result = render(request,'errorCrearCta.html',{'reason': "dejaste campos en blanco :c"})

    # finalmente retornado c:
    return result


def redirectToHome(request):
    return redirect('home')