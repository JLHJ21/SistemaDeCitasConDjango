from django.shortcuts import render, redirect

# Create your views here.


def informacion_invitado(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('inicio')

    return render(request, 'informacion.html')


def contacto_invitado(request):
    # Si ya tiene sesión no le abre esta página
    user = request.user
    if user.is_authenticated:
        # HttpResponse('<script>alert("funcionó");</script>')
        return redirect('inicio')

    return render(request, 'contacto.html')
