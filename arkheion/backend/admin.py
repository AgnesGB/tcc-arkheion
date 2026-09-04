from django.contrib import admin
from .models import (
    Pericia,
    Atributo,
    PericiaTreinada,
    AtributoFicha,
    Ataque,
    Classe,
    NivelClasseFicha,
    Origem,
    Raca,
    Habilidade,
    Ficha,
    Divindade,
)

admin.site.register(Pericia)
admin.site.register(Atributo)
admin.site.register(PericiaTreinada)
admin.site.register(AtributoFicha)
admin.site.register(Ataque)
admin.site.register(Classe)
admin.site.register(NivelClasseFicha)
admin.site.register(Origem)
admin.site.register(Raca)
admin.site.register(Habilidade)
admin.site.register(Ficha)
admin.site.register(Divindade)
