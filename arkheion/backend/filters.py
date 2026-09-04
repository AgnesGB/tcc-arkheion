from django_filters import rest_framework as filters
from .models import Ficha, Classe, Raca, Origem, Divindade, Monstro, Ataque, Habilidade


class FichaFilter(filters.FilterSet):
    """
    Filtro para o modelo Ficha.
    """

    nome = filters.CharFilter(lookup_expr="icontains")
    nivel_min = filters.NumberFilter(field_name="nivel", lookup_expr="gte")
    nivel_max = filters.NumberFilter(field_name="nivel", lookup_expr="lte")

    # Filtros por relacionamentos
    classe = filters.ModelMultipleChoiceFilter(
        field_name="classes",
        queryset=Classe.objects.all(),
    )

    raca = filters.ModelMultipleChoiceFilter(
        field_name="racas",
        queryset=Raca.objects.all(),
    )

    origem = filters.ModelMultipleChoiceFilter(
        field_name="origens",
        queryset=Origem.objects.all(),
    )

    divindade = filters.ModelChoiceFilter(
        queryset=Divindade.objects.all(),
    )

    class Meta:
        model = Ficha
        fields = ["nome", "nivel", "classe", "raca", "origem", "divindade"]


class MonstroFilter(filters.FilterSet):
    """
    Filtro para o modelo Monstro.
    """

    nome = filters.CharFilter(lookup_expr="icontains")
    nivel_min = filters.NumberFilter(field_name="nivel", lookup_expr="gte")
    nivel_max = filters.NumberFilter(field_name="nivel", lookup_expr="lte")
    nd_min = filters.NumberFilter(field_name="nd", lookup_expr="gte")
    nd_max = filters.NumberFilter(field_name="nd", lookup_expr="lte")
    tamanho = filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Monstro
        fields = ["nome", "nivel", "nd", "tamanho"]


class AtaqueFilter(filters.FilterSet):
    """
    Filtro para o modelo Ataque.
    """

    nome = filters.CharFilter(lookup_expr="icontains")
    tipo_dano = filters.CharFilter(lookup_expr="exact")
    homebrew = filters.BooleanFilter()

    class Meta:
        model = Ataque
        fields = ["nome", "tipo_dano", "homebrew"]


class HabilidadeFilter(filters.FilterSet):
    """
    Filtro para o modelo Habilidade.
    """

    nome = filters.CharFilter(lookup_expr="icontains")
    origem = filters.CharFilter(lookup_expr="exact")
    nivel_habilidade = filters.NumberFilter()
    nivel_habilidade_min = filters.NumberFilter(
        field_name="nivel_habilidade", lookup_expr="gte"
    )
    nivel_habilidade_max = filters.NumberFilter(
        field_name="nivel_habilidade", lookup_expr="lte"
    )
    ativo = filters.BooleanFilter()
    homebrew = filters.BooleanFilter()

    class Meta:
        model = Habilidade
        fields = ["nome", "origem", "nivel_habilidade", "ativo", "homebrew"]
