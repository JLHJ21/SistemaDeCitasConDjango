from django.shortcuts import render, redirect
from .forms import FormHoras, FormLugares
from .models import Horas, Lugares, Representantes, Pacientes, Consultorio, Auditoria
from usuario import models as modelsUsuario
from entrarSistema import forms as formEntrarSistema
from entrarSistema import models as modelsEntrarSistema

# PDF
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime, date


# Create your views here.


def inicioAdmin(request):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        lista_citas = Consultorio.objects.filter(
            id_cit__citas_estado=True).exclude(id_cit__estado_cita='Rechazada').distinct('id_cit').order_by('-id_cit')

        listaRoles = modelsEntrarSistema.UsuarioRoles.objects.filter(
            id_usu=request.user.id)

        return render(request, 'inicio_admin.html', {
            'listaCitas': lista_citas,
            'listaRoles': listaRoles
        })


def pdfCitas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= Lista-Citas-reporte.pdf'

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Cabecera
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 745, 'Citas')
    c.setFont('Helvetica', 12)
    c.drawString(30, 725, 'Reporte de citas realizadas')

    hoy_fecha = str(datetime.today().strftime('%Y-%m-%d'))
    hoy = "Fecha de Hoy: "+hoy_fecha

    c.setFont('Helvetica-Bold', 12)
    c.drawString(420, 750, hoy)
    c.line(415, 745, 570, 745)

    # Nombra de las listas
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    representante = Paragraph('''REPRESENTANTE''', styleBH)
    paciente = Paragraph('''PACIENTE''', styleBH)
    lugar = Paragraph('''LUGAR''', styleBH)
    fecha = Paragraph('''FECHA''', styleBH)
    estado = Paragraph('''ESTADO''', styleBH)

    data = []
    data.append([id, representante, paciente, lugar, fecha, estado])

    # consultas = [cita.id_pac for cita in lista_select]

    lista_consulta = Consultorio.objects.filter(
        id_cit__estado_cita='Realizada').distinct('id_cit').order_by('-id_cit')

    # Configuracion del contenido de la tabla
    styleN = styles["Normal"]
    styleN.alignment = TA_LEFT
    styleN.fontSize = 11
    styleN.wordWrap = 'LTR'

    high = 600
    for consulta in lista_consulta:

        if consulta.id_cit.id_pac:
            paciente = consulta.id_cit.id_pac.nombre_pac
        else:
            paciente = 'No enlazado'

        id_cita = str(consulta.id_cit.id_cit)
        representante = str(consulta.id_cit.id_usu.nombre)

        pacientes = str(paciente)

        lugar = str(consulta.id_cit.id_lugar.ubicacion_lugar)
        fecha = str(consulta.id_cit.dia_cit)

        estado_cita = str(consulta.id_cit.estado_cita)

        this_estudiante = [Paragraph(id_cita, styleBH),
                           Paragraph(representante, styleBH),
                           Paragraph(
            pacientes, styleBH),
            Paragraph(lugar, styleBH),
            Paragraph(fecha, styleBH),
            Paragraph(estado_cita, styleBH)]
        data.append(this_estudiante)
        high = high - 18

    # Contenido de la tabla
    width, height = A4
    table = Table(data, colWidths=[  # estilo de la tabla
                  1.5 * cm, 4.5 * cm, 4.5 * cm, 3.9 * cm, 2.5 * cm, 2.5 * cm])
    table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25,
                   colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))

    # tamaño del PDF
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()  # guardar pagina

    # Guardar PDF
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def pdf_representante(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= Lista-Representante-reporte.pdf'

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Cabecera
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 745, 'Representantes')
    c.setFont('Helvetica', 12)
    c.drawString(30, 725, 'Reporte de representantes')

    hoy_fecha = str(datetime.today().strftime('%Y-%m-%d'))
    hoy = "Fecha de Hoy: "+hoy_fecha

    c.setFont('Helvetica-Bold', 12)
    c.drawString(420, 750, hoy)
    c.line(415, 745, 570, 745)

    # Nombra de las listas
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    representante = Paragraph('''CORREO''', styleBH)
    paciente = Paragraph('''NOMBRE''', styleBH)
    lugar = Paragraph('''TELÉFONO''', styleBH)
    fecha = Paragraph('''CÉDULA''', styleBH)

    data = []
    data.append([id, representante, paciente, lugar, fecha])

    # consultas = [cita.id_pac for cita in lista_select]

    lista_representantes = Representantes.objects.filter(
        representante_estado=True).distinct('id_rep').order_by('-id_rep')

    # Configuracion del contenido de la tabla
    styleN = styles["Normal"]
    styleN.alignment = TA_LEFT
    styleN.fontSize = 11
    styleN.wordWrap = 'LTR'

    high = 650
    for representante in lista_representantes:

        id_rep = str(representante.id_rep)
        cedula = str(representante.id_usu.cedula)
        representante_nb = str(representante.id_usu.nombre)

        telefono = str(representante.id_usu.numero)
        email = str(representante.id_usu.correo)

        this_estudiante = [Paragraph(id_rep, styleBH),
                           Paragraph(email, styleBH),
                           Paragraph(
            representante_nb, styleBH),
            Paragraph(telefono, styleBH),
            Paragraph(cedula, styleBH)]
        data.append(this_estudiante)
        high = high - 18

    # Contenido de la tabla
    width, height = A4
    table = Table(data, colWidths=[  # estilo de la tabla
                  1.5 * cm, 4.5 * cm, 4.5 * cm, 3.9 * cm, 2.5 * cm, 2.5 * cm])
    table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25,
                   colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))

    # tamaño del PDF
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()  # guardar pagina

    # Guardar PDF
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def pdf_paciente(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= Lista-Paciente-reporte.pdf'

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Cabecera
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 745, 'Pacientes')
    c.setFont('Helvetica', 12)
    c.drawString(30, 725, 'Reporte de pacientes')

    hoy_fecha = str(datetime.today().strftime('%Y-%m-%d'))
    hoy = "Fecha de Hoy: "+hoy_fecha

    c.setFont('Helvetica-Bold', 12)
    c.drawString(420, 750, hoy)
    c.line(415, 745, 570, 745)

    # Nombra de las listas
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    id = Paragraph('''#''', styleBH)
    representante = Paragraph('''NOMBRE''', styleBH)
    paciente = Paragraph('''REPRESENTANTE''', styleBH)
    lugar = Paragraph('''FECHA DE NACIMIENTO''', styleBH)
    fecha = Paragraph('''GÉNERO''', styleBH)

    data = []
    data.append([id, representante, paciente, lugar, fecha])

    # consultas = [cita.id_pac for cita in lista_select]

    lista_pacientes = Pacientes.objects.filter(
        pacientes_pac=True).distinct('id_pac').order_by('-id_pac')

    # Configuracion del contenido de la tabla
    styleN = styles["Normal"]
    styleN.alignment = TA_LEFT
    styleN.fontSize = 11
    styleN.wordWrap = 'LTR'

    high = 650
    for paciente in lista_pacientes:

        id_rep = str(paciente.id_pac)
        nombre = str(paciente.nombre_pac)
        representante_nb = str(paciente.id_rep.id_usu.nombre)

        nacimiento = str(paciente.nacimiento_pac)
        genero = str(paciente.genero_pac)

        this_estudiante = [Paragraph(id_rep, styleBH),
                           Paragraph(nombre, styleBH),
                           Paragraph(
            representante_nb, styleBH),
            Paragraph(nacimiento, styleBH),
            Paragraph(genero, styleBH)]
        data.append(this_estudiante)
        high = high - 18

    # Contenido de la tabla
    width, height = A4
    table = Table(data, colWidths=[  # estilo de la tabla
                  1.5 * cm, 4.5 * cm, 4.5 * cm, 5.5 * cm, 2.5 * cm])
    table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25,
                   colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))

    # tamaño del PDF
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()  # guardar pagina

    # Guardar PDF
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def representantes(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        if request.method == 'GET':

            representanteAll = Representantes.objects.all()

            lista_usuarios = modelsEntrarSistema.CrearCuenta.objects.exclude(
                id__in=representanteAll).filter(usuario_estado=True)

            lista_representantes = Representantes.objects.filter(
                representante_estado=True)

            return render(request, 'representantes.html', {
                'listaUsuarios': lista_usuarios,
                'listaRepresentantes': lista_representantes,

            })
        else:

            representanteAll = Representantes.objects.all()

            lista_usuarios = modelsEntrarSistema.CrearCuenta.objects.exclude(
                id__in=representanteAll).filter(usuario_estado=True)

            lista_representantes = Representantes.objects.filter(
                representante_estado=True)

            if 'btnUpdateRepresentante' in request.POST:
                # print(request.POST)
                instance_User = modelsEntrarSistema.CrearCuenta.objects.get(
                    id=request.POST['id_usu_select'])

                idRep = Representantes.objects.get(
                    id_rep=request.POST['id_rep'])
                idRep.id_usu = instance_User
                idRep.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se actualizó el usuario relacionado ({request.POST['id_usu_select']}) de un 'representante' en la tabla *Representante*, con el id {request.POST['id_rep']},  actualizado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            elif 'btnEliminarRepresentante' in request.POST:
                idRep = Representantes.objects.get(
                    id_rep=request.POST['id_rep'])
                idRep.representante_estado = False
                idRep.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se eliminó un 'representante' en la tabla *Representantes*, con el id {request.POST['id_rep']}, eliminado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------
            else:

                instance_User = modelsEntrarSistema.CrearCuenta.objects.get(
                    id=request.POST['id_usu'])

                idRep = Representantes(id_usu=instance_User)

                idRep.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se creado un 'representante' en la tabla *Representantes*, relacionado con el usuario ({request.POST['id_usu']}), con el id {idRep.pk}, creado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

        return render(request, 'representantes.html', {
            'listaUsuarios': lista_usuarios,
            'listaRepresentantes': lista_representantes,
        })


def pacientes(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        if request.method == 'GET':

            lista_pacientes = Pacientes.objects.filter(pacientes_pac=True)
            lista_representantes = Representantes.objects.filter(
                representante_estado=True)

            return render(request, 'pacientes.html', {
                'listaRepresentantes': lista_representantes,
                'listaPacientes': lista_pacientes,
            })
        else:
            lista_pacientes = Pacientes.objects.filter(pacientes_pac=True)
            lista_representantes = Representantes.objects.filter(
                representante_estado=True)
            if 'btnUpdatePaciente' in request.POST:
                # print(request.POST)
                instance_Representante = Representantes.objects.get(
                    id_rep=request.POST['id_rep'])

                idPac = Pacientes.objects.get(id_pac=request.POST['id_pac'])
                # idPac.id_rep = instance_Representante

                idPac.nombre_pac = request.POST['nombre_pac']
                idPac.nacimiento_pac = request.POST['nacimiento_pac']
                idPac.genero_pac = request.POST['genero_pac']
                idPac.id_rep = instance_Representante

                idPac.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se actualizó el nombre ({request.POST['nombre_pac']}), el nacimiento ({request.POST['nacimiento_pac']}), genero ({request.POST['genero_pac']}) y el representante ({request.POST['id_rep']}) de un 'paciente' en la tabla *Paciente*, con el id {request.POST['id_pac']},  actualizado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            elif 'btnDeletePaciente' in request.POST:
                idRep = Pacientes.objects.get(id_pac=request.POST['id_pac'])
                idRep.pacientes_pac = False
                idRep.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se eliminó un 'paciente' en la tabla *Paciente*, con el id {request.POST['id_pac']}, eliminado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            else:

                hoy_dia = date.today().strftime('%Y-%m-%d')

                instance_Representante = Representantes.objects.get(
                    id_rep=request.POST['id_rep'])

                if hoy_dia < (request.POST['nacimiento_pac']):
                    error = "No puedes colocar una fecha mayor a la de hoy"
                    return render(request, 'pacientes.html', {
                        'listaRepresentantes': lista_representantes,
                        'listaPacientes': lista_pacientes,
                        'error': error
                    })
                else:

                    idPac = Pacientes(
                        id_rep=instance_Representante, nombre_pac=request.POST['nombre_pac'], nacimiento_pac=request.POST['nacimiento_pac'],  genero_pac=request.POST['genero_pac'])
                    idPac.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se creado un 'paciente' en la tabla *Paciente*, relacionado con el representante ({request.POST['id_rep']}), con el id {idPac.pk}, creado por el usuario: {request.user.id},")
                    Audi.save()

                    # fin de trigger ----

        return render(request, 'pacientes.html', {
            'listaRepresentantes': lista_representantes,
            'listaPacientes': lista_pacientes,

        })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def consultorio_cita(request):
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        if request.method == 'GET':
            csrf_variable = request.GET.get('csrfmiddlewaretoken')

            lista_select = modelsUsuario.Citas.objects.filter(
                id_cit=request.GET['id_cit'])

            consultas = [cita.id_pac for cita in lista_select]
            print(type(consultas))

            if None in consultas:
                lista_consulta = ''
                print("none")
            else:
                lista_consulta = Consultorio.objects.filter(
                    id_cit__id_pac=consultas[0], id_cit__estado_cita='Realizada')
                print("else")

            return render(request, 'consultorio_citas.html', {
                'citaSelect': lista_select,
                'listaPrevia': lista_consulta

            })

        else:
            print(request.POST)
            instance_Citas = modelsUsuario.Citas.objects.get(
                id_cit=request.POST['id_cit'])

            if request.POST['nacimiento_hidden'] == 'nada':
                idCon = Consultorio(
                    id_cit=instance_Citas, peso_con=request.POST['peso_con'], altura_con=request.POST['altura_con'],  nota_con=request.POST['nota_con'])

            else:
                naci = request.POST['nacimiento_hidden']
                idCon = Consultorio(
                    id_cit=instance_Citas, peso_con=request.POST['peso_con'], altura_con=request.POST['altura_con'],  nota_con=request.POST['nota_con'], nacimiento_con=naci)

            idCon.save()

            idCit = modelsUsuario.Citas.objects.get(
                id_cit=request.POST['id_cit'])
            idCit.estado_cita = "Realizada"
            idCit.save()

            # Aqui ponemos el codigo del trigger -------

            Audi = Auditoria(
                descripcion_aut=f"Se creado una 'consulta' en la tabla *Consultorio*, con el peso del paciente {request.POST['peso_con']} y con la nota de la consulta ({request.POST['nota_con']}) con el id {idCon.pk}, creado por el usuario: {request.user.id},")
            Audi.save()

            # fin de trigger ------

            print("hecho")
            return redirect('consultorio')
        return redirect('inicioAdmin')


def consultorio(request):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    lista_select = modelsUsuario.Citas.objects.filter(
        citas_estado=True, estado_cita='Aceptada', id_cit=9)

    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        if request.method == 'GET':

            lista_citas = modelsUsuario.Citas.objects.filter(
                citas_estado=True, estado_cita='Aceptada', dia_cit=datetime.today()).order_by('-id_cit')
            lista_consultorio = modelsUsuario.Citas.objects.filter(
                citas_estado=True, estado_cita='Aceptada')

            return render(request, 'consultorio.html', {
                'listaCitas': lista_citas,
                'citaSelect': lista_select,
                'listaConsultorio': lista_consultorio,
                'fecha': fecha_hoy
            })
        else:

            lista_citas = modelsUsuario.Citas.objects.filter(
                citas_estado=True, estado_cita='Aceptada')
            lista_consultorio = modelsUsuario.Citas.objects.filter(
                citas_estado=True, estado_cita='Aceptada')
            print("error")

            instance_Citas = modelsUsuario.Citas.objects.get(
                id_cit=request.POST['id_cit'])

            idCon = Consultorio(id_cit=instance_Citas, peso_con=request.POST['peso_con'],
                                altura_con=request.POST['altura_con'],  nota_con=request.POST['nota_con'])
            idCon.save()

            idCit = modelsUsuario.Citas(id_cit=request.POST['id_cit'])
            idCit.estado_cita = "Realizada"
            idCit.save()

            # Aqui ponemos el codigo del trigger -------

            Audi = Auditoria(
                descripcion_aut=f"Se creado una 'consulta' en la tabla *Consultorio*, con el peso del paciente {request.POST['peso_con']} y con la nota de la consulta ({request.POST['nota_con']}) con el id {idCon.pk}, creado por el usuario: {request.user.id},")
            Audi.save()

            # fin de trigger ------

        return render(request, 'consultorio.html', {
            'listaCitas': lista_citas,
            'citaSelect': lista_select,
            'listaConsultorio': lista_consultorio,
            'fecha': fecha_hoy

        })


def citas_admin(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        if request.method == 'GET':

            lista_citas_aceptadas = modelsUsuario.Citas.objects.filter(
                estado_cita='Aceptada', citas_estado=True)
            lista_citas_rechazadas = modelsUsuario.Citas.objects.filter(
                estado_cita='Rechazada', citas_estado=True)
            lista_citas_pendientes = modelsUsuario.Citas.objects.filter(
                estado_cita='Sin confirmar', citas_estado=True)
            lista_citas_realizadas = modelsUsuario.Citas.objects.filter(
                estado_cita='Realizada', citas_estado=True)

            return render(request, 'citas_admin.html', {
                'listaCitasAceptadas': lista_citas_aceptadas,
                'listaCitasRechazadas': lista_citas_rechazadas,
                'listaCitasPendientes': lista_citas_pendientes,
                'listaCitasRealizadas': lista_citas_realizadas,


            })
        else:

            lista_citas_aceptadas = modelsUsuario.Citas.objects.filter(
                estado_cita='Aceptada', citas_estado=True)
            lista_citas_rechazadas = modelsUsuario.Citas.objects.filter(
                estado_cita='Rechazada', citas_estado=True)
            lista_citas_pendientes = modelsUsuario.Citas.objects.filter(
                estado_cita='Sin confirmar', citas_estado=True)

            if 'btnRevisarAceptar' in request.POST:
                print(request.POST)
                idCita = modelsUsuario.Citas.objects.get(
                    id_cit=request.POST['id_cit'])
                idCita.estado_cita = 'Aceptada'
                idCita.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se aceptó una 'cita' en la tabla *Citas*, con el id {request.POST['id_cit']}, aceptado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            elif 'btnRevisarRechazar' in request.POST:
                idCita = modelsUsuario.Citas.objects.get(
                    id_cit=request.POST['id_cit'])
                idCita.estado_cita = 'Rechazada'
                idCita.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se rechazó una 'cita' en la tabla *Citas*, con el id {request.POST['id_cit']}, rechazado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            elif 'btnAceptadaRechazar' in request.POST:
                idCita = modelsUsuario.Citas.objects.get(
                    id_cit=request.POST['id_cit'])
                idCita.estado_cita = 'Rechazada'
                idCita.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se rechazó una 'cita' antes aceptada, en la tabla *Citas*, con el id {request.POST['id_cit']}, rechazado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            elif 'btnRechazarAceptar' in request.POST:
                idCita = modelsUsuario.Citas.objects.get(
                    id_cit=request.POST['id_cit'])
                idCita.estado_cita = 'Aceptada'
                idCita.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se aceptó una 'cita' antes rechazada, en la tabla *Citas*, con el id {request.POST['id_cit']}, rechazado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

            elif 'btnRechazarEliminar' in request.POST:
                idCita = modelsUsuario.Citas.objects.get(
                    id_cit=request.POST['id_cit'])
                idCita.citas_estado = False
                idCita.save()

                # Aqui ponemos el codigo del trigger -------

                Audi = Auditoria(
                    descripcion_aut=f"Se eliminó una 'cita' en la tabla *Citas*, con el id {request.POST['id_cit']}, eliminado por el usuario: {request.user.id},")
                Audi.save()

                # fin de trigger ------

        return render(request, 'citas_admin.html', {
            'listaCitasAceptadas': lista_citas_aceptadas,
            'listaCitasRechazadas': lista_citas_rechazadas,
            'listaCitasPendientes': lista_citas_pendientes,
        })


def cfg_admin(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_usuario:
        return redirect('inicio')
    else:
        form = formEntrarSistema.FormRegistrar()
        if request.method == 'GET':
            form = formEntrarSistema.FormRegistrar()
            return render(request, 'configuracion_admin.html', {
                'form': form
            })
        else:

            idUser = modelsEntrarSistema.CrearCuenta.objects.get(
                id=request.user.id)

            if 'btnUsuario' in request.POST:

                if modelsEntrarSistema.CrearCuenta.objects.filter(username=request.POST['username']).exists():
                    HttpResponse(
                        "<script>alert('Ya existe ese usuario')</script>")

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })
                else:
                    idUser.username = request.POST['username']
                    idUser.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio el usuario por {request.POST['username']}.")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })

            elif 'btnCedula' in request.POST:
                if modelsEntrarSistema.CrearCuenta.objects.filter(cedula=request.POST['cedula']).exists():
                    HttpResponse(
                        "<script>alert('Ya se ha registrado esta cédula')</script>")

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })
                else:
                    idUser.cedula = request.POST['cedula']
                    idUser.save()
                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio la cedula, del usuario {request.user.id} .")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })

            elif 'btnTelefono' in request.POST:

                if not request.POST['numero']:
                    HttpResponse(
                        "<script>alert('Tiene que escribir un número telefónico')</script>")

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })
                else:
                    idUser.numero = request.POST['numero']
                    idUser.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio el numero de teléfono, del usuario {request.user.id} .")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })

            elif 'btnCorreo' in request.POST:

                if modelsEntrarSistema.CrearCuenta.objects.filter(correo=request.POST['correo']).exists():
                    HttpResponse(
                        "<script>alert('Ya existe este correo')</script>")

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })
                else:
                    idUser.correo = request.POST['correo']
                    idUser.save()
                    print(idUser.save())

                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio el correo electrónico por {request.user.id}.")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })

            elif 'btnContrasenna' in request.POST:

                if not request.POST['password1'] == request.POST['password2']:
                    HttpResponse(
                        "<script>alert('Las contraseñas deben ser iguales')</script>")

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })
                else:
                    idUser.set_password(request.POST['password1'])
                    idUser.save()
                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio la contraseña por {request.user.id}.")
                    Audi.save()

                    # fin de trigger ------

                    return render(request, 'configuracion_admin.html', {
                        'form': form
                    })

            elif 'btnAll' in request.POST:
                if modelsEntrarSistema.CrearCuenta.objects.filter(correo=request.POST['correo']).exists() or modelsEntrarSistema.CrearCuenta.objects.filter(username=request.POST['username']).exists() or modelsEntrarSistema.CrearCuenta.objects.filter(cedula=request.POST['cedula']).exists():
                    HttpResponse(
                        "<script>alert('Los datos suministrados ya existen en el sistema, elija otros por favor.')</script>")
                    return render(request, 'configuracion_admin.html', {
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

                        Audi = Auditoria(
                            descripcion_aut=f"Se modifico una 'cuenta' en la tabla *CrearCuenta*, se cambio todos los datos por {request.user.id}.")
                        Audi.save()

                        # fin de trigger ------

                        return render(request, 'configuracion_admin.html', {
                            'form': form
                        })

                    else:
                        HttpResponse(
                            "<script>alert('Las contraseñas deben ser iguales')</script>")
                        return render(request, 'configuracion_admin.html', {
                            'form': form
                        })

        return render(request, 'configuracion_admin.html', {
            'form': form
        })


def cfg_ct(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        if request.method == 'GET':

            # lista_horas = Horas.objects.all()
            lista_horas = Horas.objects.filter(horas_estado=True)
            lista_lugares = Lugares.objects.filter(lugares_estado=True)

            formHoras = FormHoras()
            formLugares = FormLugares()

            return render(request, 'cfg_ct.html', {
                'formHoras': formHoras,
                'listaHoras': lista_horas,

                'formLugares': formLugares,
                'listaLugares': lista_lugares,

            })
        else:

            lista_horas = Horas.objects.filter(horas_estado=True)
            formHoras = FormHoras()

            formLugares = FormLugares()
            lista_lugares = Lugares.objects.filter(lugares_estado=True)

            if 'submitHoras' in request.POST:
                formHoras = FormHoras(request.POST)
                if formHoras.is_valid():

                    id_horas = formHoras.save()

                    print(id_horas.pk)

                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se creado una 'hora' en la tabla *Horas*, con el inicio de hora{request.POST['inicio_hora']} y final de hora {request.POST['final_hora']}, con el id {id_horas.pk}, creado por el usuario: {request.user.id},")
                    Audi.save()

                    # fin de trigger ------

                    return redirect('configuracion_citas')
                else:
                    print("")
            elif 'submitLugares' in request.POST:

                # instanceHoras = Horas.objects.get(id_hora=request.POST['id_hora'])
                # print(instanceHoras)

                formLugares = FormLugares(request.POST)

                if formLugares.is_valid():

                    idLugares = formLugares.save()

                    # Aqui ponemos el codigo del trigger -------

                    Audi = Auditoria(
                        descripcion_aut=f"Se creado un 'lugar' en la tabla *Lugares*, con la ubicación {request.POST['ubicacion_lugar']}, con el id {idLugares.pk}, creado por el usuario: {request.user.id},")
                    Audi.save()

                    # fin de trigger ------

                    return redirect('configuracion_citas')
                else:
                    print("")

        return render(request, 'cfg_ct.html', {
            'formHoras': formHoras,
            'listaHoras': lista_horas,

            'formLugares': formLugares,
            'listaLugares': lista_lugares,
        })

# CRUD DE CONFIGURACION ADMIN


def deleteHora_cfg_ct(request, id_hora):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        # idHora = Horas.objects.get(id_hora=id_hora)
        # idHora.delete()
        idHora = Horas.objects.get(id_hora=id_hora)
        idHora.horas_estado = False
        idHora.save()

        # Aqui ponemos el codigo del trigger -------

        Audi = Auditoria(
            descripcion_aut=f"Se eliminó una 'hora' en la tabla *Horas*, con el id {id_hora}, eliminado por el usuario: {request.user.id},")
        Audi.save()

        # fin de trigger ------
        return redirect('configuracion_citas')


def updateHora_cfg_ct(request, id_hora):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        idHora = Horas.objects.get(id_hora=id_hora)
        idHora.inicio_hora = request.POST['inicio_hora']
        idHora.final_hora = request.POST['final_hora']
        idHora.save()

        # Aqui ponemos el codigo del trigger -------

        Audi = Auditoria(
            descripcion_aut=f"Se actualizó el inicio({request.POST['inicio_hora']}) y final {request.POST['final_hora']} de una 'hora' en la tabla *Horas*, con el id {id_hora},  actualizado por el usuario: {request.user.id},")
        Audi.save()

        # fin de trigger ------

        return redirect('configuracion_citas')


def deleteLugar_cfg_ct(request, id_lugar):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:
        idLugar = Lugares.objects.get(id_lugar=id_lugar)
        idLugar.lugares_estado = False
        idLugar.save()

        # Aqui ponemos el codigo del trigger -------

        Audi = Auditoria(
            descripcion_aut=f"Se eliminó un 'lugar' en la tabla *Lugar*, con el id {id_lugar}, eliminado por el usuario: {request.user.id},")
        Audi.save()

        # fin de trigger ------
        return redirect('configuracion_citas')


def updateLugar_cfg_ct(request, id_lugar):

    # Si ya tiene sesión no le abre esta página
    user = request.user
    if not user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('iniciarSesion')

    tipoRol = TipoRol(request)

    if not tipoRol.es_administrador:
        return redirect('inicio')
    else:

        instanceHoras = Horas.objects.get(id_hora=request.POST['id_hora'])

        id_lugar = Lugares.objects.get(id_lugar=id_lugar)
        id_lugar.ubicacion_lugar = request.POST['ubicacion_lugar']
        id_lugar.nombre_lugar = request.POST['nombre_lugar']
        id_lugar.id_hora = instanceHoras

        id_lugar.save()

        # Aqui ponemos el codigo del trigger -------

        Audi = Auditoria(
            descripcion_aut=f"Se actualizó la ubicación ({request.POST['ubicacion_lugar']}), nombre {request.POST['nombre_lugar']} y el id de la hora ({request.POST['id_hora']}) de un 'lugar' en la tabla *Lugar*, con el id {id_lugar},  actualizado por el usuario: {request.user.id},")
        Audi.save()

        # fin de trigger ------

        return redirect('configuracion_citas')


def TipoRol(request):
    instanceHoras = formEntrarSistema.UsuarioRoles.objects.get(
        id_usu=request.user)

    return instanceHoras
