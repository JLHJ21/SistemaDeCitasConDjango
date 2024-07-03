from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import UsuarioRoles


from django.contrib.auth import get_user_model, authenticate
User = get_user_model()


class FormIniciar(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Ingresar nombre de usuario',
            'onkeypress': 'return SoloLetrasYNumerosYGuiones(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '30',
            'required': 'true',
            'name': 'username',
            'id': 'username',
        }),
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresar contraseña',
            'onkeypress': 'return SoloLetrasYNumerosYGuiones(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '30',
            'required': 'true',
            'name': 'password',
            'id': 'password',
        })

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError(
                    {'password': ["Los datos suministrados no existen."]})


class FormRegistrar(forms.Form, UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Ingresar nombre',
            'onkeypress': 'return SoloLetras(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '60',
            'required': 'true',
            'name': 'nombre',
            'id': 'nombre',
        }),
        self.fields['username'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Ingresar usuario',
            'onkeypress': 'return SoloLetrasYNumerosYGuiones(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '30',
            'required': 'true',
            'name': 'username',
            'id': 'username',
        }),
        self.fields['correo'].widget.attrs.update({
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'Ingresar Correo Electrónico',
            'onkeypress': 'return SoloCorreo(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '50',
            'required': 'true',
            'name': 'correo',
            'id': 'correo',
        }),
        self.fields['nacionalidad'].widget.attrs.update({
            'type': 'select',
            'class': 'form-select',
            'required': 'true',
            'name': 'nacionalidad',
            'id': 'nacionalidad',
        }),
        self.fields['cedula'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Ingresar cédula',
            'onkeypress': 'return SoloNumeros(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '20',
            'required': 'true',
            'name': 'cedula',
            'id': 'cedula',
        }),
        self.fields['numero'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Ingresar número de telefono. Ejemplo: 04161234567',
            'onkeypress': 'return SoloNumeros(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '20',
            'required': 'true',
            'name': 'numero',
            'id': 'numero',
        }),
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresar contraseña',
            'onkeypress': 'return SoloLetrasYNumerosYGuiones(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '30',
            'required': 'true',
            'name': 'password1',
            'id': 'password1',
        }),
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresar contraseña',
            'onkeypress': 'return SoloLetrasYNumerosYGuiones(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '30',
            'required': 'true',
            'name': 'password2',
            'id': 'password2',
        })

    nombre = forms.CharField()
    # usuario = forms.CharField()

    CHOICES = (('V-', 'V-'), ('E-', 'E-'),)
    nacionalidad = forms.ChoiceField(choices=CHOICES)

    cedula = forms.CharField()
    numero = forms.CharField()

    correo = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('nombre', 'username', 'correo', 'nacionalidad',
             'cedula', 'numero', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(FormRegistrar, self).clean()

        if not self.cleaned_data.get('password1'):
            del self.errors['password1']
            self.add_error(
                'password1', "Necesita escribir la contraseñas en ambos inputs.")
            self.add_error(
                'password2', "Necesita escribir la contraseñas en ambos inputs.")
        elif not self.cleaned_data.get('password2'):
            del self.errors['password2']
            self.add_error(
                'password1', "Necesita escribir la contraseñas en ambos inputs.")
            self.add_error(
                'password2', "Necesita escribir la contraseñas en ambos inputs.")
        else:
            if not self.cleaned_data.get('password1') == self.cleaned_data.get('password2'):
                del self.errors['password2']
                self.add_error(
                    'password2', "Las contraseñas no coinciden.")

        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            del self.errors['username']
            self.add_error(
                'username', "El usuario ya ha sido elegido, intente otro.")

        if not self.cleaned_data.get('username'):
            del self.errors['username']
            self.add_error(
                'username', "Necesita escribir un usuario.")

        if not self.cleaned_data.get('nombre'):
            del self.errors['nombre']
            self.add_error(
                'nombre', "Necesita escribir un nombre.")

        if User.objects.filter(correo=self.cleaned_data.get('correo')).exists():
            del self.errors['correo']
            self.add_error(
                'correo', "El usuario ya ha sido elegido, intente otro.")
        elif not self.cleaned_data.get('correo'):
            del self.errors['correo']
            self.add_error(
                'correo', "Necesita escribir un correo electrónico.")

        if not self.cleaned_data.get('nacionalidad'):
            del self.errors['nacionalidad']
            self.add_error(
                'nacionalidad', "Necesita elegir una nacionalidad.")

        if User.objects.filter(cedula=self.cleaned_data.get('cedula')).exists():
            del self.errors['cedula']
            self.add_error(
                'cedula', "La cédula ya ha sido elegida, intente otra.")
        elif not self.cleaned_data.get('cedula'):
            del self.errors['cedula']
            self.add_error(
                'cedula', "Necesita escribir una cedula.")

        if not self.cleaned_data.get('numero'):
            del self.errors['numero']
            self.add_error(
                'numero', "Necesita escribir un número telefónico.")
        return cleaned_data
