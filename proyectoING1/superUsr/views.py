from django.shortcuts import render, redirect
from django.http import HttpResponse
from superUsr.models import *
from usuario.models import *

# Create your views here.
def logIn_adm(request):
    correo = request.GET.get('correo', "")
    contra = request.GET.get('contra', "")

    if correo != "" and contra != "":
        if verifyLogin_adm(request, correo, contra):
            return redirect('success_adm', correo=correo)

    ctx = {
        'correo': correo
    }
    return render(request, 'logIn_adm.html', ctx)

def success_adm(request, correo):
    if verifySesion_adm(request, correo=correo):
        users = UsuariosDB.objects.all()

        bloquear = request.GET.get('1',"")
        eliminar = request.GET.get('2',"")
        desbloquear = request.GET.get('3',"")
        email = request.GET.get('email',"")

        if bloquear != "":
            manageUsr_adm(request, correo, email, r=1)
            return redirect('success_adm', correo=correo)
        if eliminar != "":
            manageUsr_adm(request, correo, email, r=2)
            return redirect('success_adm', correo=correo)
        if desbloquear != "":
            manageUsr_adm(request, correo, email, r=3)
            return redirect('success_adm', correo=correo)

        ctx = {
            'users': users,
            'correo': correo
        }
        return render(request, 'perfil_adm.html', ctx)
    else:
        return HttpResponse(f'sesion invalida')

def manageUsr_adm(request, correo, email, r):
    if verifySesion_adm(request, correo):

        try:
            user = UsuariosDB.objects.get(correo=email)
        except:
            return False

        if r==1:
            user.alive = 2
            user.save()

        if r==2:
            user.delete()
            PostsDB.objects.filter(correo=email).delete()
            MsgsDB.objects.filter(correo=email).delete()
            MsgsDB.objects.filter(correof=email).delete()
            AmigosDB.objects.filter(correo=email).delete()
            AmigosDB.objects.filter(correof=email).delete()

        if r==3:
            user.alive = 1
            user.save()
    else:
        return HttpResponse(f'sesion invalida')

def logOut_adm(request, correo):
    if verifySesion_adm(request, correo):
        uwu = AdminDB.objects.get(correo=correo)
        uwu.ip = ""
        uwu.save()
        return redirect('logIn_adm')
    else:
        return HttpResponse(f'sesion invalida')

def verifyLogin_adm(request, correo, contra):
    try:
        uwu = AdminDB.objects.get(correo=correo, contra=contra)
        uwu.ip = request.META.get('REMOTE_ADDR')
        uwu.save()
        return True
    except:
        return False

def verifySesion_adm(request, correo):
    try:
        uwu = AdminDB.objects.get(correo=correo)
        ip = request.META.get('REMOTE_ADDR')

        if ip == uwu.ip:
            return True
        else:
            return False
    except:
        return False