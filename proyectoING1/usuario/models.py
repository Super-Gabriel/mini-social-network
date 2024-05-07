from django.db import models

# Create your models here.
class UsuariosDB(models.Model):
    nombre = models.CharField(max_length=40)
    correo = models.CharField(max_length=40)
    contra = models.CharField(max_length=40)
    fecha = models.DateField(null=True)
    genero = models.CharField(max_length=1)
    isOn = models.BooleanField(default=False)
    ip = models.CharField(max_length=20, default="")
    alive = models.CharField(max_length=1, default="1")

class AmigosDB(models.Model):
    correo = models.CharField(max_length=40)
    correof = models.CharField(max_length=40)
    pending = models.CharField(max_length=1)

class PostsDB(models.Model):
    correo = models.CharField(max_length=40)
    post = models.CharField(max_length=500)
    hora = models.DateTimeField(auto_now_add=True)

class MsgsDB(models.Model):
    correo = models.CharField(max_length=40)
    correof = models.CharField(max_length=40)
    msg = models.CharField(max_length=100)
    hora = models.DateTimeField(auto_now_add=True)