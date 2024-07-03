"""
URL configuration for DjangoProyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from invitado import views as invitado_views
from entrarSistema import views as entrarSistema_views
from usuario import views as usuario_views
from administrador import views as administrador_views
from programador import views as programador_views


urlpatterns = [
    path('admin/', admin.site.urls),



    path('', invitado_views.informacion_invitado,
         name='informacion_invitado'),



    path('contacto/', invitado_views.contacto_invitado,
         name='contacto_invitado'),
    path('entrar/', entrarSistema_views.iniciarSesion, name='iniciarSesion'),
    path('registrar/', entrarSistema_views.Registrarse, name='registrarse'),

    path('inicio/', usuario_views.inicio, name='inicio'),
    path('deleteCita/<int:id_cit>/',
         usuario_views.deleteCita_historial, name='deleteCita'),


    path('cita/', usuario_views.cita, name='cita'),
    path('historial/', usuario_views.historial, name='historial'),
    path('configuracion/', usuario_views.configuracion, name='configuracion'),
    path('cerrar/', entrarSistema_views.cerrarSesion, name='cerrar'),
    path('inicio_admin/', administrador_views.inicioAdmin, name='inicioAdmin'),
    path('representantes/',
         administrador_views.representantes, name='representantes'),
    path('pacientes/', administrador_views.pacientes, name='pacientes'),

    path('consultorio/', administrador_views.consultorio, name='consultorio'),
    path('consultorio_cita/',
         administrador_views.consultorio_cita, name='consultorio_cita'),


    path('citas_admin/', administrador_views.citas_admin, name='citas_admin'),

    path('cfg_ct/', administrador_views.cfg_ct, name='configuracion_citas'),
    # deleteHora
    path('deleteHora/<int:id_hora>/',
         administrador_views.deleteHora_cfg_ct, name='eliminarHora'),
    path('updateHora/<int:id_hora>/',
         administrador_views.updateHora_cfg_ct, name='updateHora'),
    path('updateLugar/<int:id_lugar>/',
         administrador_views.updateLugar_cfg_ct, name='updateLugar'),
    path('deleteLugar/<int:id_lugar>/',
         administrador_views.deleteLugar_cfg_ct, name='deleteLugar'),

    path('cfg_admin/', administrador_views.cfg_admin, name='configuracion_admin'),

    path('inicio_programador/', programador_views.inicio_programador,
         name='inicio_programador'),

    path('roles_programador/', programador_views.roles_programador,
         name='roles_programador'),

    # PDF
    path('pdf_citas/', administrador_views.pdfCitas, name='pdf_citas'),
    path('pdf_representante/', administrador_views.pdf_representante,
         name='pdf_representante'),
    path('pdf_paciente/', administrador_views.pdf_paciente, name='pdf_paciente'),




]
