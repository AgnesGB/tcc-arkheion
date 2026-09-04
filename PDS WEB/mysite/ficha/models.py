from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Pericia(models.Model):
    PERICIA = [
        ("acr", "Acrobacia"),  # Destreza
        ("ade", "Adestramento"),  # Carisma
        ("atl", "Atletismo"),  # Força
        ("atu", "Atuação"),  # Carisma
        ("cav", "Cavalgar"),  # Destreza
        ("con", "Conhecimento"),  # Inteligência
        ("cur", "Cura"),  # Sabedoria
        ("dip", "Diplomacia"),  # Carisma
        ("eng", "Enganação"),  # Carisma
        ("for", "Fortitude"),  # Constituição
        ("fur", "Furtividade"),  # Destreza
        ("gue", "Guerra"),  # Inteligência
        ("ini", "Iniciativa"),  # Destreza
        ("int", "Intimidação"),  # Carisma
        ("inu", "Intuição"),  # Sabedoria
        ("inv", "Investigação"),  # Inteligência
        ("jog", "Jogatina"),  # Carisma
        ("lad", "Ladinagem"),  # Destreza
        ("lut", "Luta"),  # Força
        ("mis", "Misticismo"),  # Inteligência
        ("nob", "Nobreza"),  # Inteligência
        ("ofi", "Ofício"),  # Inteligência
        ("per", "Percepção"),  # Sabedoria
        ("pil", "Pilotagem"),  # Destreza
        ("pon", "Pontaria"),  # Destreza
        ("ref", "Reflexos"),  # Destreza
        ("rel", "Religião"),  # Sabedoria
        ("sob", "Sobrevivência"),  # Sabedoria
        ("von", "Vontade"),  # Sabedoria
    ]
    nome = models.CharField(
        max_length=3, choices=PERICIA, verbose_name="Perícia"
    )  # fazer responsivo
    requer_treino = models.BooleanField(verbose_name="Requer treino?", default=False)

    def __str__(self):
        return self.get_nome_display()


class Atributo(models.Model):
    ATRIBUTO = [
        ("for", "Força"),
        ("des", "Destreza"),
        ("con", "Constituição"),
        ("int", "Inteligência"),
        ("sab", "Sabedoria"),
        ("car", "Carisma"),
    ]
    nome = models.CharField(max_length=3, choices=ATRIBUTO, verbose_name="Atributo")
    ordem = models.IntegerField(default=1)

    def __str__(self):
        return self.get_nome_display()


class PericiaTreinada(models.Model):
    ficha = models.ForeignKey("Ficha", on_delete=models.SET_NULL, null=True, blank=True)
    pericia = models.ForeignKey(
        "Pericia", on_delete=models.SET_NULL, null=True, blank=True
    )
    atributo_chave = models.ManyToManyField(
        "AtributoFicha", verbose_name="Atributo Chave", related_name="atributoChave"
    )  # uma pericia possui muitos atributos, um atributo está em diversas pericias.
    treinado = models.BooleanField(default=False, verbose_name="Treinado")
    bonus_adicional = models.IntegerField(default=0)

    def __str__(self):
        return self.pericia.nome

    def verificarTreino(self):
        bonus_treino = 0

        if self.treinado:
            if self.ficha.nivel >= 0 and self.ficha.nivel <= 5:
                bonus_treino = 2
            elif self.ficha.nivel >= 6 and self.ficha.nivel <= 14:
                bonus_treino = 4
            elif self.ficha.nivel >= 15:
                bonus_treino = 6

        return bonus_treino

    def calcularValor(self):
        if not self.ficha:
            return 0
        if self.pericia.requer_treino == True and self.treinado == False:
            return 0

        atributo_total = sum(attr.valor for attr in self.atributo_chave.all())

        valor = (
            ((self.ficha.nivel) // 2)
            + atributo_total
            + self.verificarTreino()
            + self.bonus_adicional
        )
        return valor

    def adicionarBonus(self, int):
        self.bonus_pericia = int
        return self.calcularValor() + int


class AtributoFicha(models.Model):
    atributo = models.ForeignKey(
        "Atributo", on_delete=models.SET_NULL, null=True, blank=True
    )
    ficha = models.ForeignKey("Ficha", on_delete=models.CASCADE, null=True, blank=True)
    valor = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.atributo.nome


class Ataque(models.Model):
    TIPO_DO_DANO = [
        ("imp", "Impacto"),
        ("per", "Perfuração"),
        ("cor", "Corte"),
        ("men", "Mental"),
        ("acd", "Ácido"),
        ("ele", "Eletricidade"),
        ("esc", "Essência"),
        ("fog", "Fogo"),
        ("fri", "Frio"),
        ("luz", "Luz"),
        ("tre", "Trevas"),
        ("ven", "Veneno"),
    ]
    nome = models.CharField(max_length=200, verbose_name="Nome do Ataque")
    descricao = models.TextField(verbose_name="Descrição do Ataque")
    dano = models.CharField(max_length=200, verbose_name="Dano")
    tipo_dano = models.CharField(
        max_length=3, choices=TIPO_DO_DANO, verbose_name="Tipo de Dano"
    )
    pericia = models.ForeignKey(
        "Pericia", on_delete=models.SET_NULL, null=True, blank=True
    )
    resistencia = models.CharField(
        max_length=200, verbose_name="Resistencia", default="---"
    )

    def __str__(self):
        return self.nome


class Classe(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    descricao = models.TextField("Descrição de Classe", null=True, blank=True)
    proficiencia = models.TextField(verbose_name="Proficiências")
    vida_base = models.IntegerField(default=0, verbose_name="Vida base")
    vida_por_nivel = models.IntegerField(default=0, verbose_name="Vida por nivel")
    mana_base = models.IntegerField(default=0, verbose_name="Mana base")
    mana_por_nivel = models.IntegerField(default=0, verbose_name="Mana por nivel")
    pericias_treinadas = models.TextField(
        verbose_name="Perícias Treinadas", null=True, blank=True
    )
    pericias_para_escolher = models.TextField(
        verbose_name="Perícias para escolher", null=True, blank=True
    )

    def __str__(self):
        return self.nome


class NivelClasseFicha(models.Model):
    classe = models.ForeignKey(
        "Classe", on_delete=models.SET_NULL, null=True, blank=True
    )
    ficha = models.ForeignKey("Ficha", on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.IntegerField(default=1, verbose_name="Nivel")

    def __str__(self):
        return self.ficha.nome


class Origem(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    descricao = models.TextField("Descrição de Origem", null=True, blank=True)
    poderes_concedidos_origem = models.CharField(
        max_length=200, verbose_name="Poderes Concedidos", null=True, blank=True
    )

    def __str__(self):
        return self.nome


class Raca(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    descricao = models.TextField("Descrição de Raça", null=True, blank=True)
    poderes_concedidos_raca = models.CharField(
        max_length=200, verbose_name="Poderes Concedidos", null=True, blank=True
    )

    def __str__(self):
        return self.nome


class Habilidade(models.Model):
    ORIGEM = [
        ("rc", "Raça"),
        ("or", "Origem"),
        ("cl", "Classe"),
        ("ge", "Geral"),
        ("de", "Destino"),
        ("to", "Tormenta"),
        ("ou", "Outro"),
    ]
    nome = models.CharField(max_length=200)
    descricao = models.TextField("Descrição do Habilidade")
    origem = models.CharField(max_length=2, choices=ORIGEM)
    ativo = models.BooleanField(default=False)
    nivel_habilidade = models.IntegerField(
        default=0, verbose_name="Nível da Habilidade"
    )
    raca_pers = models.ForeignKey(
        Raca,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Raça de origem",
    )
    origem_pers = models.ForeignKey(
        Origem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Origem de origem",
    )
    classe_pers = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Classe de origem",
    )

    def __str__(self):
        return self.nome


class Ficha(models.Model):
    DIVINDADES = [
        ("NO", "Nenhuma"),
        ("AH", "Aharadak, Deus da Tormenta"),
        ("AL", "Allihanna, Deusa da Natureza"),
        ("AR", "Arsenal, Deus da Guerra"),
        ("AZ", "Azgher, Deus do Sol"),
        ("HY", "Hyninn, Deus da Trapaça"),
        ("KA", "Kallyadranoch, Deus dos Dragões"),
        ("KH", "Khalmyr, Deus da Justiça"),
        ("LE", "Lena, Deusa da Vida"),
        ("LI", "Lin-Wu, Deus da Honra"),
        ("MA", "Marah, Deusa da Paz"),
        ("ME", "Megalokk, Deus dos Monstros"),
        ("NI", "Nimb, Deus do Caos"),
        ("OC", "Oceano, Deus do Oceano"),
        ("SS", "Sszzaas, Deus da Traição"),
        ("TA", "Tanna-Toh, Deusa do Conhecimento"),
        ("TE", "Tenebra, Deusa da Noite"),
        ("TH", "Thwor, Deus dos Goblinóides"),
        ("TY", "Thyatis, Deus da Ressurreição"),
        ("VA", "Valkaria, Deusa da Ambição"),
        ("WY", "Wynna, Deusa da Magia"),
    ]

    dono = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200, verbose_name="Nome")
    nivel = models.IntegerField(default=0, verbose_name="Nível")
    divindade = models.CharField(
        max_length=2, choices=DIVINDADES, verbose_name="Divindade"
    )
    cd = models.CharField(
        max_length=200, default="10", verbose_name="Classe de Dificuldade de Magias"
    )
    ca = models.CharField(
        max_length=200, default="10", verbose_name="Classe de Armadura"
    )
    vida_atual = models.IntegerField(default=0, verbose_name="Vida Atual")
    mana_atual = models.IntegerField(default=0, verbose_name="Mana Atual")
    exp = models.IntegerField(default=0, verbose_name="Experiência")
    deslocamento = models.CharField(
        max_length=50, default="9 metros/ 6 quadrados", verbose_name="Deslocamento"
    )
    tamanho = models.CharField(max_length=50, default="Médio", verbose_name="Tamanho")

    # relacionamentos
    atributos = models.ManyToManyField(
        Atributo, through="AtributoFicha"
    )  # uma ficha possui muitos atributos, um atributo está em diversas fichas.
    habilidades = models.ManyToManyField(
        Habilidade
    )  # uma ficha possui muitas habilidades, uma habilidade está em diversas fichas.
    racas = models.ManyToManyField(
        Raca
    )  # uma ficha possui uma raça, uma raça está em diversas fichas.
    origens = models.ManyToManyField(
        Origem
    )  # uma ficha possui uma origem, uma origem está em diversas fichas.
    classes = models.ManyToManyField(
        Classe, through="NivelClasseFicha", related_name="classeFicha"
    )  # uma ficha possui muitas classes, uma classe está em diversas fichas.
    ataques = models.ManyToManyField(
        Ataque
    )  # uma ficha possui muitos ataques, um ataque está em diversas fichas.
    pericias = models.ManyToManyField(
        Pericia, through="PericiaTreinada", related_name="periciaTreinada"
    )  # uma ficha possui muitas pericias, uma pericia está em diversas fichas.

    def __str__(self):
        return self.nome

    def calcularVida(self):
        # Obtém o valor da Constituição
        const = 0
        atributo_const = self.atributoficha_set.filter(atributo__nome="con").first()
        if atributo_const:
            const = atributo_const.valor

        # Obtém todas as classes da ficha
        niveis_classes = self.nivelclasseficha_set.all()

        if not niveis_classes.exists():
            return 10  # Valor padrão caso não tenha classe

        # Vida base da primeira classe + Constituição
        primeira_classe = niveis_classes.first()
        vida_total = primeira_classe.classe.vida_base + const

        # Adiciona vida por nível para cada classe
        for nivel_classe in niveis_classes:
            vida_total += nivel_classe.classe.vida_por_nivel * nivel_classe.nivel

        return vida_total - primeira_classe.classe.vida_por_nivel

    def calcularMana(self):
        # Obtém todas as classes da ficha
        niveis_classes = self.nivelclasseficha_set.all()

        if not niveis_classes.exists():
            return 0  # Valor padrão caso não tenha classe

        mana_total = 0

        # Adiciona mana por nível para cada classe
        for nivel_classe in niveis_classes:
            mana_total += nivel_classe.classe.mana_por_nivel * nivel_classe.nivel

        return mana_total

    def setarNivel(self, args):
        self.nivel = args
        self.calcular_todas_pericias()

    def subirUmNivel(self):
        self.nivel = self.nivel + 1
        self.calcular_todas_pericias()

    def calcular_todas_pericias(self):
        pericias_valores = {}
        for pericia_treinada in self.periciatreinada_set.all():
            pericias_valores[pericia_treinada.pericia.nome] = (
                pericia_treinada.calcularValor()
            )
        return pericias_valores
