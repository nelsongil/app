from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Clientes(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    correo = models.EmailField()
    tel1 = models.CharField(max_length=20)
    tel2 = models.CharField(max_length=20, blank=True)
    notas = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'app_Clientes'

    def __str__(self):
        return self.apellido + ', ' + self.nombre


class Obras(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, null=True)
    dir = models.CharField(max_length=100)
    notas = models.CharField(max_length=200)
    tel = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_Obras'


class MaterialesF(models.Model):
    nombre = models.CharField(max_length=40)
    descrip = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_MaterialesF'
    
    def __str__(self):
        return self.nombre


class Materiales(models.Model):
    familia = models.ForeignKey(MaterialesF, models.DO_NOTHING, null=True)
    nombre = models.CharField(max_length=40)
    descrip = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_Materiales'

    
class Horas(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    tipo = models.CharField(max_length=3)
    latitud = models.CharField(default=1, max_length=15)
    longitud = models.CharField(default=1, max_length=15)
    idUsuario = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    class Meta:
        db_table = 'app_Horas'
