from django.shortcuts import render, redirect
from administrador import views as administradorViews
from administrador import models as administradorModels
from entrarSistema import models as entrarSistemaModels

# Create your views here.


def inicio_programador(request):
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = administradorViews.TipoRol(request)

    if not tipoRol.es_programador:
        return redirect('inicio')

    if request.method == 'GET':

        lista_auditoria = administradorModels.Auditoria.objects.all().order_by('-id_aut')
        listaRoles = entrarSistemaModels.UsuarioRoles.objects.filter(
            id_usu=request.user.id)

        return render(request, 'inicio_progr.html', {
            'auditorias': lista_auditoria,
            'listaRoles': listaRoles
        })


def roles_programador(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = administradorViews.TipoRol(request)

    if not tipoRol.es_programador:
        return redirect('inicio')

    if request.method == 'GET':

        listaUsuarios = entrarSistemaModels.CrearCuenta.objects.all()

        listaUserRoles = entrarSistemaModels.UsuarioRoles.objects.filter(
            id_usu__in=listaUsuarios)

        listaRoles = entrarSistemaModels.UsuarioRoles.objects.filter(
            id_usu=request.user.id)

        return render(request, 'roles_progr.html', {
            'listaRoles': listaRoles,
            'listaUsuarios': listaUserRoles
        })
    else:

        listaUsuarios = entrarSistemaModels.CrearCuenta.objects.all()

        listaUserRoles = entrarSistemaModels.UsuarioRoles.objects.filter(
            id_usu__in=listaUsuarios)

        listaRoles = entrarSistemaModels.UsuarioRoles.objects.filter(
            id_usu=request.user.id)

        print(request.POST)
        if 'option1' in request.POST:
            rol = entrarSistemaModels.UsuarioRoles.objects.get(
                id_usu=request.user.id)
            rol.es_usuario = True
            rol.save()
            print("1")
        if 'option2' in request.POST:
            rol = entrarSistemaModels.UsuarioRoles.objects.get(
                id_usu=request.user.id)
            rol.es_administrador = True
            rol.save()
            print("2")
        else:
            rol = entrarSistemaModels.UsuarioRoles.objects.get(
                id_usu=request.user.id)
            rol.es_administrador = False
            rol.save()
            print("2")

        if 'option3' in request.POST:
            rol = entrarSistemaModels.UsuarioRoles.objects.get(
                id_usu=request.user.id)
            rol.es_programador = True
            rol.save()
            print("3")
        else:
            rol = entrarSistemaModels.UsuarioRoles.objects.get(
                id_usu=request.user.id)
            rol.es_programador = False
            rol.save()
            print("3")

    return render(request, 'roles_progr.html', {
        'listaRoles': listaRoles,
        'listaUsuarios': listaUserRoles
    })
