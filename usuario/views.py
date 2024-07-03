from django.shortcuts import render, redirect
from administrador import models as modelsAdministrador
from administrador import views as viewsAdministrador
from .forms import FormCitas
from entrarSistema import forms as formsEntrarSistema
from entrarSistema import models as modelsEntrarSistema
from .models import Citas
from django.http import HttpResponse


# Create your views here.


def inicio(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        return redirect('iniciarSesion')

    tipoRol = viewsAdministrador.TipoRol(request)

    if not tipoRol.es_usuario:
        return redirect('cerrar')
    else:

        if request.method == 'GET':

            formCitas = FormCitas()

            # lista_horas = Horas.objects.all()
            lista_horas = modelsAdministrador.Horas.objects.filter(
                horas_estado=True)
            lista_lugares = modelsAdministrador.Lugares.objects.filter(
                lugares_estado=True)
            lista_citas = Citas.objects.filter(
                id_usu=request.user.id, citas_estado=True).order_by('-id_cit')

            listaRoles = modelsEntrarSistema.UsuarioRoles.objects.filter(
                id_usu=request.user.id)

            return render(request, 'inicio.html', {
                'form': formCitas,

                'listaHoras': lista_horas,
                'listaLugares': lista_lugares,
                'listaCitas': lista_citas,
                'listaRoles': listaRoles
            })
        else:
            # formCitas = FormCitas()

            lista_horas = modelsAdministrador.Horas.objects.filter(
                horas_estado=True)
            lista_lugares = modelsAdministrador.Lugares.objects.filter(
                lugares_estado=True)
            lista_citas = Citas.objects.filter(
                id_usu=request.user.id, citas_estado=True)

            id_cita = Citas.objects.get(id_cit=request.POST['id_cit'])
            id_hora = modelsAdministrador.Horas.objects.get(
                id_hora=request.POST['id_hora'])
            id_lugar = modelsAdministrador.Lugares.objects.get(
                id_lugar=request.POST['id_lugar'])

            print(request.POST['id_pac'])

            if request.POST['id_pac'] == 'nada':
                pass
            else:
                id_pac = modelsAdministrador.Pacientes.objects.get(
                    id_pac=request.POST['id_pac'])
                id_cita.id_pac = id_pac
            id_cita.dia_cit = request.POST['dia_cit']
            id_cita.nota_cit = request.POST['nota_cit']
            id_cita.id_hora = id_hora
            id_cita.id_lugar = id_lugar

            id_cita.save()
            # Aqui ponemos el codigo del trigger -------

            Audi = modelsAdministrador.Auditoria(
                descripcion_aut=f"Se modificó una 'cita' en la tabla *Citas*, para el día {request.POST['dia_cit']}, modificado por el usuario: {request.user.id},")
            Audi.save()

            # fin de trigger ------
            return redirect('inicio')

        return render(request, 'inicio.html', {
            'form': formCitas,

            'listaHoras': lista_horas,
            'listaLugares': lista_lugares,
            'listaCitas': lista_citas,
        })


def deleteCita_historial(request, id_cit):
    user = request.user
    if not user.is_authenticated:
        return redirect('iniciarSesion')

    tipoRol = viewsAdministrador.TipoRol(request)

    if not tipoRol.es_usuario:
        return redirect('cerrar')
    else:
        idCita = Citas.objects.get(id_cit=id_cit)
        idCita.citas_estado = False
        idCita.save()

        # Aqui ponemos el codigo del trigger -------

        Audi = modelsAdministrador.Auditoria(
            descripcion_aut=f"Se eliminó una 'cita' en la tabla *Citas*, para el día {idCita.dia_cit} y con el id {id_cit}, eliminado por el usuario: {request.user.id},")
        Audi.save()

        # fin de trigger ------
        return redirect('inicio')


def cita(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        return redirect('iniciarSesion')

    tipoRol = viewsAdministrador.TipoRol(request)

    if not tipoRol.es_usuario:
        return redirect('cerrar')
    else:

        if request.method == 'GET':
            formCitas = FormCitas()

            # lista_horas = Horas.objects.all()
            lista_horas = modelsAdministrador.Horas.objects.filter(
                horas_estado=True)
            lista_lugares = modelsAdministrador.Lugares.objects.filter(
                lugares_estado=True)

            representantes = modelsAdministrador.Representantes.objects.filter(
                id_usu=request.user.id, representante_estado=True)
            id_rep = [representante.id_rep for representante in representantes]

            lista_pacientes = modelsAdministrador.Pacientes.objects.filter(
                id_rep__id_usu=request.user.id, pacientes_pac=True)

            print(id_rep)
            return render(request, 'citas.html', {
                'form': formCitas,

                'listaHoras': lista_horas,
                'listaLugares': lista_lugares,
                'listaPacientes': lista_pacientes
            })
        else:
            formCitas = FormCitas()

            lista_horas = modelsAdministrador.Horas.objects.filter(
                horas_estado=True)
            lista_lugares = modelsAdministrador.Lugares.objects.filter(
                lugares_estado=True)

            instance_User = modelsEntrarSistema.CrearCuenta.objects.get(
                id=request.POST['id_usu'])

            instance_Lugar = modelsAdministrador.Lugares.objects.get(
                id_lugar=request.POST['id_lugar'])

            instance_Hora = modelsAdministrador.Horas.objects.get(
                id_hora=request.POST['id_hora'])

            if Citas.objects.filter(dia_cit=request.POST['dia_cit'], id_usu=request.POST['id_usu']).exists():

                error = "No puedes hacer dos citas un mismo día"
                return render(request, 'citas.html', {
                    'error': error
                })
            else:
                print("no existe")

            if request.POST['id_pac'] == 'nada':
                id_cita = Citas(id_usu=instance_User, id_lugar=instance_Lugar, id_hora=instance_Hora,
                                dia_cit=request.POST['dia_cit'], nota_cit=request.POST['nota_cit'], estado_cita='Sin confirmar')
            else:
                instance_Paciente = modelsAdministrador.Horas.objects.get(
                    id_hora=request.POST['id_hora'])
                id_cita = Citas(id_usu=instance_User, id_lugar=instance_Lugar, id_hora=instance_Hora,
                                id_pac=instance_Paciente, dia_cit=request.POST['dia_cit'], nota_cit=request.POST['nota_cit'], estado_cita='Sin confirmar')

            id_cita.save()

            # Aqui ponemos el codigo del trigger -------

            Audi = modelsAdministrador.Auditoria(
                descripcion_aut=f"Se creó una 'cita' en la tabla *Citas*, para el día {request.POST['dia_cit']} y con el id {id_cita.pk}, creado por el usuario: {request.user.id},")
            Audi.save()

            # fin de trigger ------

            return redirect('cita')

        return render(request, 'citas.html', {
            'form': formCitas,

            'listaHoras': lista_horas,
            'listaLugares': lista_lugares,
        })


def historial(request):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = viewsAdministrador.TipoRol(request)

    if not tipoRol.es_usuario:
        return redirect('cerrar')
    else:

        if request.method == 'GET':

            lista_citas = modelsAdministrador.Consultorio.objects.filter(
                id_cit__id_usu=request.user.id, id_cit__citas_estado=True)

            return render(request, 'historial.html', {
                'listaCitas': lista_citas,
            })


def configuracion(request):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = viewsAdministrador.TipoRol(request)

    if not tipoRol.es_usuario:
        return redirect('cerrar')
    else:
        form = formsEntrarSistema.FormRegistrar()
        if request.method == 'GET':
            form = formsEntrarSistema.FormRegistrar()
            return render(request, 'configuracion.html', {
                'form': form
            })
        else:

            idUser = modelsEntrarSistema.CrearCuenta.objects.get(
                id=request.user.id)

            if 'btnUsuario' in request.POST:

                if modelsEntrarSistema.CrearCuenta.objects.filter(username=request.POST['username']).exists():
                    HttpResponse(
                        "<script>alert('Ya existe ese usuario')</script>")

                    return render(request, 'configuracion.html', {
                        'form': form
                    })
                else:
                    idUser.username = request.POST['username']
                    idUser.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = modelsAdministrador.Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio el usuario por {request.POST['username']}.")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion.html', {
                        'form': form
                    })

            elif 'btnCedula' in request.POST:
                if modelsEntrarSistema.CrearCuenta.objects.filter(cedula=request.POST['cedula']).exists():
                    HttpResponse(
                        "<script>alert('Ya se ha registrado esta cédula')</script>")

                    return render(request, 'configuracion.html', {
                        'form': form
                    })
                else:
                    idUser.cedula = request.POST['cedula']
                    idUser.save()
                    # Aqui ponemos el codigo del trigger -------

                    Audi = modelsAdministrador.Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio la cedula, del usuario {request.user.id} .")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion.html', {
                        'form': form
                    })

            elif 'btnTelefono' in request.POST:

                if not request.POST['numero']:
                    HttpResponse(
                        "<script>alert('Tiene que escribir un número telefónico')</script>")

                    return render(request, 'configuracion.html', {
                        'form': form
                    })
                else:
                    idUser.numero = request.POST['numero']
                    idUser.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = modelsAdministrador.Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio el numero de teléfono, del usuario {request.user.id} .")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion.html', {
                        'form': form
                    })

            elif 'btnCorreo' in request.POST:

                if modelsEntrarSistema.CrearCuenta.objects.filter(correo=request.POST['correo']).exists():
                    HttpResponse(
                        "<script>alert('Ya existe este correo')</script>")

                    return render(request, 'configuracion.html', {
                        'form': form
                    })
                else:
                    idUser.correo = request.POST['correo']
                    idUser.save()
                    print(idUser.save())

                    # Aqui ponemos el codigo del trigger -------

                    Audi = modelsAdministrador.Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio el correo electrónico por {request.user.id}.")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion.html', {
                        'form': form
                    })

            elif 'btnContrasenna' in request.POST:

                if not request.POST['password1'] == request.POST['password2']:
                    HttpResponse(
                        "<script>alert('Las contraseñas deben ser iguales')</script>")

                    return render(request, 'configuracion.html', {
                        'form': form
                    })
                else:
                    idUser.set_password(request.POST['password1'])
                    idUser.save()
                    # Aqui ponemos el codigo del trigger -------

                    Audi = modelsAdministrador.Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio la contraseña por {request.user.id}.")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion.html', {
                        'form': form
                    })

            elif 'btnAll' in request.POST:
                if modelsEntrarSistema.CrearCuenta.objects.filter(correo=request.POST['correo']).exists() or modelsEntrarSistema.CrearCuenta.objects.filter(username=request.POST['username']).exists() or modelsEntrarSistema.CrearCuenta.objects.filter(cedula=request.POST['cedula']).exists():
                    HttpResponse(
                        "<script>alert('Los datos suministrados ya existen en el sistema, elija otros por favor.')</script>")
                    return render(request, 'configuracion.html', {
                        'form': form
                    })
                else:
                    if request.POST['password1'] == request.POST['password2']:

                        idUser.username = request.POST['username']
                        idUser.cedula = request.POST['cedula']
                        idUser.numero = request.POST['numero']
                        idUser.correo = request.POST['correo']
                        idUser.set_password(request.POST['password1'])
                        idUser.save()

                        # Aqui ponemos el codigo del trigger -------

                        Audi = modelsAdministrador.Auditoria(
                            descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio todos los datos por {request.user.id}.")
                        Audi.save()

                        # fin de trigger ------

                        return render(request, 'configuracion.html', {
                            'form': form
                        })

                    else:
                        HttpResponse(
                            "<script>alert('Las contraseñas deben ser iguales')</script>")
                        return render(request, 'configuracion.html', {
                            'form': form
                        })

        return render(request, 'configuracion.html', {
            'form': form
        })
