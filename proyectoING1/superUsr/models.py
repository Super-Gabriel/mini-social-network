from django.db import models

# Create your models here.
class AdminDB(models.Model):
    correo = models.CharField(max_length=40)
    contra = models.CharField(max_length=40)
    ip = models.CharField(max_length=20, default="")