from django.contrib import admin
from .models import (
    Ficha,
    Pericia,
    Atributo,
    Ataque,
    Classe,
    Origem,
    Raca,
    Habilidade,
    PericiaTreinada,
    AtributoFicha,
    NivelClasseFicha,
)

admin.site.register(Ficha)
admin.site.register(Pericia)
admin.site.register(Atributo)
admin.site.register(Classe)
admin.site.register(Origem)
admin.site.register(Ataque)
admin.site.register(Habilidade)
admin.site.register(Raca)
admin.site.register(PericiaTreinada)
admin.site.register(AtributoFicha)
admin.site.register(NivelClasseFicha)
