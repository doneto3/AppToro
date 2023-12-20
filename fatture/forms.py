from django import forms
from django.utils.safestring import mark_safe
from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import Fattura, Cliente, Viaggio


class TassaForm(forms.ModelForm):
    class Meta:
        model = Fattura
        fields = ['numero', 'data', 'importo','tipo']

    def __init__(self, *args, **kwargs):
        super(TassaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['readonly'] = True
        self.fields['tipo'].required = False
        self.fields['tipo'].widget = forms.HiddenInput()
        self.fields['tipo'].initial = 'T'

class BurocraziaForm(forms.ModelForm):
    class Meta:
        model = Fattura
        fields = ['numero', 'data', 'importo','tipo']

    def __init__(self, *args, **kwargs):
        super(BurocraziaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['readonly'] = True
        self.fields['tipo'].required = False
        self.fields['tipo'].widget = forms.HiddenInput()
        self.fields['tipo'].initial = 'B'

class UscitaForm(forms.ModelForm):
    class Meta:
        model = Fattura
        fields = ['numero', 'data', 'importo','tipo']

    def __init__(self, *args, **kwargs):
        super(UscitaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['readonly'] = True
        self.fields['tipo'].required = False
        self.fields['tipo'].widget = forms.HiddenInput()
        self.fields['tipo'].initial = 'S'


class EntrataForm(forms.ModelForm):
    class Meta:
        model = Fattura
        fields = ['numero', 'data', 'cliente','viaggi','importo','tipo']


    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id',None)
        super(EntrataForm, self).__init__(*args, **kwargs)

        self.fields['tipo'].widget.attrs['readonly'] = True
        self.fields['tipo'].required = False

        self.fields['tipo'].initial = 'C'
        self.fields['viaggi'].widget.attrs['readonly'] = True
        self.fields['viaggi'].required = False
        self.fields['viaggi'].queryset = Viaggio.objects.all().exclude(stato=1)

        self.fields['cliente'].widget.attrs['readonly'] = True
        self.fields['cliente'].required = False


        self.fields['importo'].widget.attrs['readonly'] = True
        self.fields['importo'].required = False


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome']


class ViaggioForm(forms.ModelForm):

    class Meta:
        model = Viaggio
        fields = ['data_viaggio','distanza_km','ddt','prezzo_viaggio','cliente','mittente']

    def __init__(self, *args, **kwargs):

        numero = kwargs.pop('numero', None)
        super(ViaggioForm, self).__init__(*args, **kwargs)

        self.fields['mittente'].queryset = Cliente.objects.all().exclude(nome='Inalca')
        if numero == 1:
            self.fields['cliente'].initial = Cliente.objects.get(nome='Inalca')
            self.fields['cliente'].widget.attrs['readonly'] = True
            self.fields['cliente'].required = False
        else:
            self.fields['cliente'].queryset = Cliente.objects.all().exclude(nome='Inalca')

