from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuario.models import *
from django.db.models import Q

# Create your views here.
def inicioSesion(request):
    return render(request, 'iniciarSesionUsr.html')

    
def perfil(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contra = request.POST.get('contra')

        try:
            usuario = UsuariosDB.objects.get(correo=correo, contra=contra)
            if verifyLogin(request, correo):
                usuario.isOn = True
                usuario.ip = request.META.get('REMOTE_ADDR')
                usuario.save()
                return redirect('perfil_success', correo=correo)

            return HttpResponse('ya hay una sesión iniciada o estas bloqueado')
            
        except UsuariosDB.DoesNotExist:
            return render(request, 'iniciarSError.html')
    else:
        return render(request, 'perfil.html')

def edit(request, correo):
    if verifySesion(request, correo=correo):

        newNombre = request.GET.get('newNombre',"")
        contra = request.GET.get('contra',"")
        newContra = request.GET.get('newContra',"")
        newCorreo = request.GET.get('newCorreo',"")

        reason = ""
        recharge = False
        if contra != "":
            if newNombre != "":
                if changeData(request, correo, contra, 'name', newNombre):
                    reason = reason + ", nombre cambiado"

            if newCorreo != "":
                if changeData(request, correo, contra, 'correo', newCorreo):
                    reason = reason + ", correo cambiado"
                    correo = newCorreo
                    recharge = True
                else:
                    reason = reason + "correo no cambiado"

            if newContra != "":
                if changeData(request, correo, contra, 'contra', newContra):
                    reason = reason + ", contraseña cambiada"
            
            if recharge: return redirect('edit', newCorreo)

        user = UsuariosDB.objects.get(correo=correo)

        ctx = {
            'user': user,
            'reason': reason,
            'correo': correo
        }
        return render(request, 'perfil_edit.html', ctx)
    else:
        return HttpResponse(f'sesion invalida')

def changeData(request, correo, contra, r, value):
    if verifySesion(request, correo):
        usuario = UsuariosDB.objects.get(correo=correo)

        if usuario.contra == contra:
            if r=='name':
                usuario.nombre = value
            
            if r=='contra':
                usuario.contra = value

            if r=='correo':
                try:
                    UsuariosDB.objects.get(correo=value)
                    return False
                except:
                    True
                #cambiando los correos de los posts
                posts = PostsDB.objects.filter(correo=correo)
                for user in posts:
                    user.correo = value
                    user.save()
                #cambiando los correos de los mensajes
                msgs = MsgsDB.objects.filter(correo=correo)
                for user in msgs:
                    user.correo = value
                    user.save()
                msgs = MsgsDB.objects.filter(correof=correo)
                for user in msgs:
                    user.correof = value
                    user.save()
                #cambiando los correos de los amigos
                friends = AmigosDB.objects.filter(correo=correo)
                for user in friends:
                    user.correo = value
                    user.save()
                friends = AmigosDB.objects.filter(correof=correo)
                for user in friends:
                    user.correof = value
                    user.save()
                usuario.correo = value

            usuario.save()
            return True
        else:
            return False
    else:
        return HttpResponse(f'sesion invalida')

def perfil_success(request, correo):
    if verifySesion(request, correo):
        post = request.GET.get('post')
        status = ""
        
        # si hay un post escrito unu
        if post != "" and post != None:
            status = publicar_post(request, correo, post)
            return redirect('perfil_success', correo = correo)

        # querys uwu
        amigos = AmigosDB.objects.filter(correo=correo, pending=3).values_list('correof', flat=True)
        posts = PostsDB.objects.filter(correo__in=amigos).order_by('-hora')
        ownPosts = PostsDB.objects.filter(correo=correo).order_by('-hora')

        ctx = {
            'correo': correo,
            'status': status,
            'posts': posts,
            'ownPosts': ownPosts
        }
        return render(request, 'perfil_success.html', ctx)
    
    return HttpResponse(f'sesion invalida')
    

def publicar_post(request, correo, post):
    if verifySesion:
        try:
            PostsDB(correo=correo, post=post).save()
            return "publicado con exito c:"
        except:
            return "algo salió mal en la base de datos"
    else:
        return HttpResponse(f'sesion invalida')


def logOut(request, correo):
    if verifySesion(request, correo):
        usuario = UsuariosDB.objects.get(correo=correo)
        usuario.isOn = False
        usuario.ip = ""
        usuario.save()
        return redirect('inicioSesion')
    return HttpResponse (f'sesion invalida')


def friends(request, correo):
    if verifySesion(request, correo):

        friends = AmigosDB.objects.filter(correo=correo, pending=3)
        reqs = AmigosDB.objects.filter(correo=correo, pending=2)
        pending = AmigosDB.objects.filter(correo=correo, pending=1)

        correo1 = request.GET.get('correo1', "")
        respond_reqs1 = request.GET.get('1', "")
        respond_reqs2 = request.GET.get('2', "")
        respond_email = request.GET.get('email', "")
        friend_req = ""

        if correo1 != "":
            friend_req = send_friend_req(request, correo, correo1)

        if respond_reqs1 != "":
            respond_reqs(request, correo=correo, email=respond_email, r=1)

        if respond_reqs2 != "":
            respond_reqs(request, correo=correo, email=respond_email, r=2)

        ctx = {
            'correo': correo,
            'friends': friends,
            'pending': pending,
            'reqs': reqs,
            'status': friend_req
        }
        return render(request, 'perfil_friends.html', ctx)
    return HttpResponse(f'sesion invalida')


def respond_reqs(request, correo, email, r):
    
    if verifySesion(request, correo):
        try:
            solicitud = AmigosDB.objects.get(correo=correo, correof=email)
            solicitud1 = AmigosDB.objects.get(correo=email, correof=correo)
        except:
            return HttpResponse(f'solicitud no valida')
        if r==1:# aceptar soli
            solicitud.pending = 3
            solicitud1.pending = 3
            solicitud.save()
            solicitud1.save()

        else:# rechazar soli
            solicitud.delete()
            solicitud1.delete()

    else:
        return HttpResponse(f'sesion invalida')


def send_friend_req(request, correo, correo1):
    if verifySesion(request, correo):
        if verifyFriendReq(request, correo, correo1):
            AmigosDB(correo=correo, correof=correo1, pending=1).save()
            AmigosDB(correo=correo1, correof=correo, pending=2).save()
            return "enviada con exito"
        return "correo invalido"
    return HttpResponse(f'sesion invalida')


def chats(request, correo):
    if verifySesion(request, correo):

        friends = AmigosDB.objects.filter(correo=correo, pending=3)
        ctx = {
            'correo': correo,
            'friends': friends
        }
        return render(request, 'perfil_chats.html', ctx)
    else:
        return HttpResponse(f'sesion invalida')


def inbox(request, correo, correo1):
    if verifySesion(request, correo):
        msg = request.GET.get('msg')

        if msg != "" and msg != None:
            send_msg(request, correo, correo1, msg)
            return redirect('inbox', correo=correo, correo1=correo1)

        fullMsgs = MsgsDB.objects.filter(Q(correo=correo, correof=correo1) | Q(correo=correo1, correof=correo))
        fullMsgs.order_by('hora')
        ctx = {
            'correo': correo,
            'correo1': correo1,
            'fullMsgs': fullMsgs
        }
        return render(request, 'perfil_inbox.html', ctx)
    else:
        return HttpResponse(f'sesion invalida')

def send_msg(request, correo, correo1, msg):
    if verifySesion(request, correo):
        MsgsDB(correo=correo, correof=correo1, msg=msg).save()
    else:
        return HttpResponse(f'sesion invalida')

def actualizar(request):
    return render(request, 'actEoo.html')


def verifyFriendReq(request, correo, correo1):
        if correo == correo1:
            return False

        try:# si el correo no está en la DB
            UsuariosDB.objects.get(correo=correo1)
        except:
            return False

        amigos = AmigosDB.objects.filter(correo=correo)
        amigosf = amigos.filter(correof=correo1)
        if not amigosf.exists():# si aun no tiene el amigo
            return True
        else:
            return False

def verifySesion(request, correo):
    try:
        usuario = UsuariosDB.objects.get(correo=correo)
        ip = request.META.get('REMOTE_ADDR')
    except UsuariosDB.DoesNotExist:
        return False

    if usuario.isOn == False:
        return False

    if usuario.ip != ip:
        return False
    
    if usuario.alive == '2':
        return False

    return True

def verifyLogin(request, correo):
    usuario = UsuariosDB.objects.get(correo=correo)

    if usuario.isOn == True:
        return False

    if usuario.alive == '2':
        return False

    return True

def prueba(request):
    x = request.GET.get('post')
    if x=="":
        return HttpResponse(f'df')
    return render(request, 'prueba.html', {'x': x})