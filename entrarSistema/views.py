from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
# from django.contrib.auth.hashers import make_password, check_password
from .forms import FormRegistrar, FormIniciar
from .models import UsuarioRoles
from administrador import views as modelsAdministrador


# Create your views here.


def iniciarSesion(request):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('inicio')
    if request.method == 'GET':
        form = FormIniciar()

        return render(request, 'entrar.html', {
            'form': form,
        })
    else:
        form = FormIniciar(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            cuenta = authenticate(username=username, password=password)

            if cuenta:
                login(request, cuenta)

                # current_user = request.user
                # print(current_user)
                if not UsuarioRoles.objects.filter(id_usu=request.user).exists():
                    # print(request.user)
                    # print("no existe")
                    roles = UsuarioRoles(id_usu=request.user)
                    roles.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = modelsAdministrador.Auditoria(
                        descripcion_aut=f"Se creó un 'rol' en la tabla *UsuarioRoles*, obteniendo permisos de usuario ({roles.es_usuario}), con el id {roles.pk}, creado por el usuario: {request.user.id},")
                    Audi.save()

                    # fin de trigger ------

                return redirect('inicio')
        else:
            print("")
            # form = FormIniciar()

    return render(request, 'entrar.html', {
        'form': form,
    })


def Registrarse(request):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('inicio')

    if request.method == 'GET':
        form = FormRegistrar()
        return render(request, 'registrar.html', {
            'form': form
        })
    else:
        form = FormRegistrar(request.POST)
        if form.is_valid():

            print(type(form))
            id_crear = form.save()

            # Aqui ponemos el codigo del trigger -------

            Audi = modelsAdministrador.Auditoria(
                descripcion_aut=f"Se creó una 'cuenta' en la tabla *CrearCuenta*, con el nombre {id_crear.nombre}, usuario {id_crear.username} y la cédula {id_crear.cedula}, creado por el usuario: {request.user.id},")
            Audi.save()

            # fin de trigger ------
            return redirect('iniciarSesion')
        else:
            print("")

    return render(request, 'registrar.html', {
        'form': form,
    })


def cerrarSesion(request):
    logout(request)
    return redirect('informacion_invitado')
    # return render(request, 'cerrar.html')
