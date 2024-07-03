from django.db import models


# Create your models here.


class Consultorio(models.Model):

    id_con = models.AutoField(primary_key=True)
    id_cit = models.ForeignKey(
        to='usuario.Citas', null=True, blank=True, on_delete=models.CASCADE)
    peso_con = models.IntegerField()
    altura_con = models.CharField(max_length=100)
    nota_con = models.TextField()
    nacimiento_con = models.DateField(null=True)
    consultorio_estado = models.BooleanField(default=True)


class Representantes(models.Model):

    id_rep = models.AutoField(primary_key=True)
    id_usu = models.ForeignKey(
        to='entrarSistema.CrearCuenta', null=True, blank=True, on_delete=models.CASCADE)
    representante_estado = models.BooleanField(default=True)


class Pacientes(models.Model):

    id_pac = models.AutoField(primary_key=True)
    id_rep = models.ForeignKey(
        Representantes, null=True, blank=True, on_delete=models.CASCADE)
    nombre_pac = models.CharField(max_length=255)
    nacimiento_pac = models.DateField()
    genero_pac = models.CharField(max_length=20)
    pacientes_pac = models.BooleanField(default=True)


class Horas(models.Model):

    id_hora = models.AutoField(primary_key=True)
    inicio_hora = models.TimeField()
    final_hora = models.TimeField()
    horas_estado = models.BooleanField(default=True)


class Lugares(models.Model):
    id_lugar = models.AutoField(primary_key=True)
    id_hora = models.ForeignKey(
        Horas, null=True, blank=True, on_delete=models.CASCADE)
    ubicacion_lugar = models.CharField(max_length=255)
    nombre_lugar = models.CharField(max_length=255)
    lugares_estado = models.BooleanField(default=True)


class Auditoria(models.Model):
    id_aut = models.AutoField(primary_key=True)
    descripcion_aut = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
