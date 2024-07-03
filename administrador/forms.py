from django import forms
from .models import Horas, Lugares
from django.forms import ModelForm


class FormHoras(forms.Form, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['inicio_hora'].widget.attrs.update({
            'type': 'time',
            'class': 'form-control',
            'required': 'true',
            'name': 'inicio_hora',
            'id': 'inicio_hora',
        }),
        self.fields['final_hora'].widget.attrs.update({
            'type': 'time',
            'class': 'form-control',
            'required': 'true',
            'name': 'final_hora',
            'id': 'final_hora',
        })

    inicio_hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}))
    final_hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta():
        model = Horas
        fields = ('inicio_hora', 'final_hora')

    def clean(self):
        cleaned_data = super(FormHoras, self).clean()

        if not self.cleaned_data.get('inicio_hora'):
            del self.errors['inicio_hora']
            self.add_error(
                'inicio_hora', "Necesita elegir una hora inicial.")
        elif not self.cleaned_data.get('final_hora'):
            del self.errors['final_hora']
            self.add_error(
                'final_hora', "Necesita elegir una hora final.")
        elif self.cleaned_data.get('inicio_hora') == self.cleaned_data.get('final_hora'):
            self.add_error(
                'inicio_hora', "Ambas fechas no tienen que ser las mismas.")
            self.add_error(
                'final_hora', "Ambas fechas no tienen que ser las mismas.")
        return cleaned_data


class FormLugares(forms.Form, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ubicacion_lugar'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'required': 'true',
            'name': 'ubicacion_lugar',
            'id': 'ubicacion_lugar',
            'placeholder': 'Ej: Cárdenas',
            'onkeypress': 'return SoloLetras(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '60',
        }),
        self.fields['nombre_lugar'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'required': 'true',
            'name': 'nombre_lugar',
            'id': 'nombre_lugar',
            'placeholder': 'Ej: Centro Médico Santos',
            'onkeypress': 'return SoloLetras(event);',
            'onpaste': 'return false;',
            'minlength': '3',
            'maxlength': '60',

        })

    ubicacion_lugar = forms.CharField(max_length=255)
    nombre_lugar = forms.CharField(max_length=255)

    class Meta():
        model = Lugares
        fields = ('id_hora', 'ubicacion_lugar', 'nombre_lugar')

    def clean(self):
        cleaned_data = super(FormLugares, self).clean()

        if not self.cleaned_data.get('id_hora'):
            del self.errors['id_hora']
            self.add_error(
                'id_hora', "Necesita elegir una hora.")
        elif not self.cleaned_data.get('ubicacion_lugar'):
            del self.errors['ubicacion_lugar']
            self.add_error(
                'ubicacion_lugar', "Necesita escribir la ubicación del lugar.")
        elif not self.cleaned_data.get('nombre_lugar'):
            del self.errors['nombre_lugar']
            self.add_error(
                'nombre_lugar', "Necesita escribir el nombre del lugar.")

        elif Lugares.objects.filter(ubicacion_lugar=self.cleaned_data.get('ubicacion_lugar')).exists():
            self.add_error(
                'ubicacion_lugar', "El lugar ya ha sido registrado.")
        return cleaned_data
