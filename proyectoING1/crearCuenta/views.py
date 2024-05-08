from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.models import *
import re
from datetime import datetime

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

        # verificando email valido
        if verifyEmail(request, corr):
            True
        else:
            return  render(request,'errorCrearCta.html',{'reason': "correo invalido"})

        # verificando fecha valida
        if verifyFecha(request, fecha):
            True
        else:
            return  render(request,'errorCrearCta.html',{'reason': "fecha invalida"})

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

def verifyFecha(request, fecha):
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    fechaNow = datetime.now().date()
    if fecha < fechaNow:
        return True
    return False
    

def verifyEmail(request, correo):
     # Expresión regular para verificar la estructura de un correo electrónico
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Verificar si el correo cumple con la estructura
    if re.match(email_regex, correo):
        return True
    else:
        return False

def redirectToHome(request):
    return redirect('home')