from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings


class ControladorCrearCuenta(BaseUserManager):
    def create_user(self, usuario, nombre, correo, nacionalidad, cedula, numero, password=None):
        if not usuario:
            raise ValueError("Debe ingresar un usuario único")
        if not nombre:
            raise ValueError("Debe ingresar un nombre válido")
        if not correo:
            raise ValueError("Debe ingresar un correo válido")
        if not cedula:
            raise ValueError("Debe ingresar una cedula válida")
        if not numero:
            raise ValueError("Debe ingresar un numero válido")

        user = self.model(
            correo=self.normalize_email(correo),
            usuario=usuario,
            nombre=nombre,
            nacionalidad=nacionalidad,
            cedula=cedula,
            numero=numero
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, usuario, nombre, correo,  password, nacionalidad, cedula, numero):
        user = self.model(
            correo=self.normalize_email(correo),
            usuario=usuario,
            nombre=nombre,
            password=password,
            nacionalidad=nacionalidad,
            cedula=cedula,
            numero=numero,
        )
        user.set_password(user.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CrearCuenta(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255, unique=True)
    nacionalidad = models.CharField(max_length=20)
    cedula = models.CharField(max_length=255, unique=True)
    numero = models.CharField(max_length=255)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    usuario_estado = models.BooleanField(default=True, null=True)

    USERNAME_FIELD = 'username'  # LOGIN
    REQUIRED_FIELDS = ['nombre', 'correo',
                       'nacionalidad', 'cedula', 'numero']  # REGISTER

    objects = ControladorCrearCuenta()

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True


class UsuarioRoles(models.Model):

    id_rol = models.AutoField(primary_key=True)
    id_usu = models.ForeignKey(
        CrearCuenta, null=True, blank=True, on_delete=models.CASCADE)
    es_usuario = models.BooleanField(default=True)
    es_administrador = models.BooleanField(default=False)
    es_programador = models.BooleanField(default=False)
