from django.db import models


# Create your models here.


class Citas(models.Model):

    id_cit = models.AutoField(primary_key=True)
    id_usu = models.ForeignKey(
        to='entrarSistema.CrearCuenta', null=True, blank=True, on_delete=models.CASCADE)
    id_lugar = models.ForeignKey(to='administrador.Lugares', null=True,
                                 blank=True, on_delete=models.CASCADE)  # SEGUIR TOCANDO
    id_hora = models.ForeignKey(to='administrador.Horas', null=True,
                                blank=True, on_delete=models.CASCADE)  # SEGUIR TOCANDO
    id_pac = models.ForeignKey(to='administrador.Pacientes', null=True,
                               blank=True, on_delete=models.CASCADE)  # SEGUIR TOCANDO
    dia_cit = models.DateField()
    nota_cit = models.TextField()
    estado_cita = models.CharField(max_length=100,)
    citas_estado = models.BooleanField(default=True)
