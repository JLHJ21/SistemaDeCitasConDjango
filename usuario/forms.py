from django import forms
from .models import Citas
from django.forms import ModelForm
from datetime import date


class FormCitas(forms.Form, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta():
        model = Citas
        fields = ('id_usu', 'id_lugar', 'id_hora', 'id_pac',
                  'dia_cit', 'nota_cit', 'estado_cita')

    def clean(self):
        cleaned_data = super(FormCitas, self).clean()
        fecha_hoy = date.today()

        if not self.cleaned_data.get('id_lugar'):
            del self.errors['id_lugar']
            self.add_error(
                'id_lugar', "Necesita elegir un lugar.")
        elif not self.cleaned_data.get('id_hora'):
            del self.errors['id_hora']
            self.add_error(
                'id_hora', "Necesita elegir una hora.")

        elif not self.cleaned_data.get('dia_cit'):
            del self.errors['dia_cit']
            self.add_error(
                'dia_cit', "Necesita elegir un día de la cita.")
        elif Citas.objects.filter(dia_cit=self.cleaned_data.get('dia_cit'), id_usu=self.cleaned_data.get('id_usu')).exists():
            del self.errors['id_hora']
            self.add_error(
                'id_hora', "Solo una cita al día.")
        elif not self.cleaned_data.get('nota_cit'):
            del self.errors['nota_cit']
            self.add_error(
                'nota_cit', "Necesita escribir una nota.")
        return cleaned_data
