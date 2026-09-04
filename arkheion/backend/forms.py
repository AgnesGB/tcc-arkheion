from django import forms
from .models import (
    Ficha,
    AtributoFicha,
    PericiaTreinada,
    Ataque,
    Classe,
    NivelClasseFicha,
    Origem,
    Raca,
    Habilidade,
)


class FichaForm(forms.ModelForm):
    class Meta:
        model = Ficha
        fields = "__all__"


class AtributoFichaForm(forms.ModelForm):
    class Meta:
        model = AtributoFicha
        fields = "__all__"


class PericiaTreinadaForm(forms.ModelForm):
    class Meta:
        model = PericiaTreinada
        fields = "__all__"


class AtaqueForm(forms.ModelForm):
    class Meta:
        model = Ataque
        fields = "__all__"


class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = "__all__"


class NivelClasseFichaForm(forms.ModelForm):
    class Meta:
        model = NivelClasseFicha
        fields = "__all__"


class OrigemForm(forms.ModelForm):
    class Meta:
        model = Origem
        fields = "__all__"


class RacaForm(forms.ModelForm):
    class Meta:
        model = Raca
        fields = "__all__"


class HabilidadeForm(forms.ModelForm):
    class Meta:
        model = Habilidade
        fields = "__all__"
