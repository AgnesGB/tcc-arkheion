from django.db import models
from django.contrib.auth.models import User


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
        if self.pericia.requer_treino is True and self.treinado is False:
            return 0

        atributo_total = sum(attr.valor for attr in self.atributo_chave.all())

        valor = (
            ((self.ficha.nivel) // 2)
            + atributo_total
            + self.verificarTreino()
            + self.bonus_adicional
        )
        return valor

    def adicionarBonus(self, bonus):
        return self.calcularValor() + bonus


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
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ataques_homebrew",
    )
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
    homebrew = models.BooleanField(default=False, verbose_name="Homebrew?")

    def __str__(self):
        return self.nome


class Classe(models.Model):
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="classes_homebrew",
    )
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
    homebrew = models.BooleanField(default=False, verbose_name="Homebrew?")

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
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="origens_homebrew",
    )
    nome = models.CharField(max_length=200, verbose_name="Nome")
    descricao = models.TextField("Descrição de Origem", null=True, blank=True)
    homebrew = models.BooleanField(default=False, verbose_name="Homebrew?")

    def __str__(self):
        return self.nome


class Raca(models.Model):
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="racas_homebrew",
    )
    nome = models.CharField(max_length=200, verbose_name="Nome")
    descricao = models.TextField("Descrição de Raça", null=True, blank=True)
    homebrew = models.BooleanField(default=False, verbose_name="Homebrew?")

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
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="habilidades_homebrew",
    )
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
    divindade_pers = models.ForeignKey(
        "Divindade",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Divindade de origem",
    )
    homebrew = models.BooleanField(default=False, verbose_name="Homebrew?")

    def __str__(self):
        return self.nome


class Divindade(models.Model):
    # DIVINDADES =
    # 'Aharadak, Deus da Tormenta'
    # 'Allihanna, Deusa da Natureza'
    # 'Arsenal, Deus da Guerra'
    # 'Azgher, Deus do Sol'
    # 'Hyninn, Deus da Trapaça'
    # 'Kallyadranoch, Deus dos Dragões'
    # 'Khalmyr, Deus da Justiça'
    # 'Lena, Deusa da Vida'
    # 'Lin-Wu, Deus da Honra'
    # 'Marah, Deusa da Paz'
    # 'Megalokk, Deus dos Monstros'
    # 'Nimb, Deus do Caos'
    # 'Oceano, Deus do Oceano'
    # 'Sszzaas, Deus da Traição'
    # 'Tanna-Toh, Deusa do Conhecimento'
    # 'Tenebra, Deusa da Noite'
    # 'Thwor, Deus dos Goblinóides'
    # 'Thyatis, Deus da Ressurreição'
    # 'Valkaria, Deusa da Ambição'
    # 'Wynna, Deusa da Magia'
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="divindades_homebrew",
    )
    nome = models.CharField(max_length=200, verbose_name="Nome da Divindade")
    descricao = models.TextField("Descrição da Divindade", null=True, blank=True)
    simbolo = models.CharField(
        "Símbolo da Divindade", max_length=200, null=True, blank=True
    )
    obrigacoes = models.TextField("Obrigações da Divindade", null=True, blank=True)
    restrições = models.TextField("Restrições da Divindade", null=True, blank=True)
    homebrew = models.BooleanField(default=False, verbose_name="Homebrew?")

    def __str__(self):
        return self.nome


class Ficha(models.Model):
    dono = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200, verbose_name="Nome")
    nivel = models.IntegerField(default=0, verbose_name="Nível")
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
    divindade = models.ForeignKey(
        Divindade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Divindade",
        related_name="divindade_ficha",
    )

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


class MonstroPericia(models.Model):
    monstro = models.ForeignKey(
        "Monstro", on_delete=models.CASCADE, null=True, blank=True
    )
    pericia = models.ForeignKey(
        "Pericia", on_delete=models.SET_NULL, null=True, blank=True
    )
    atributo_chave = models.ManyToManyField(
        "AtributoMonstro",
        verbose_name="Atributo Chave",
        related_name="atributoChaveMonstro",
    )  # uma pericia possui muitos atributos, um atributo está em diversas pericias.

    def __str__(self):
        return self.pericia.nome


class AtributoMonstro(models.Model):
    atributo = models.ForeignKey(
        "Atributo", on_delete=models.SET_NULL, null=True, blank=True
    )
    monstro = models.ForeignKey(
        "Monstro", on_delete=models.CASCADE, null=True, blank=True
    )
    valor = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.atributo.nome


class Monstro(models.Model):

    dono = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200, verbose_name="Nome")
    nivel = models.IntegerField(default=0, verbose_name="Nível")
    nd = models.IntegerField(default=0, verbose_name="Nível de Dificuldade")
    cd = models.CharField(
        max_length=200,
        default="10",
        verbose_name="Classe de Dificuldade de Magias",
        null=True,
        blank=True,
    )
    ca = models.CharField(
        max_length=200,
        default="10",
        verbose_name="Classe de Armadura",
        null=True,
        blank=True,
    )
    vida = models.IntegerField(default=0, verbose_name="Vida Atual")
    mana = models.IntegerField(default=0, verbose_name="Mana Atual")
    deslocamento = models.CharField(
        max_length=50, default="9 metros/ 6 quadrados", verbose_name="Deslocamento"
    )
    tamanho = models.CharField(max_length=50, default="Médio", verbose_name="Tamanho")

    # relacionamentos
    atributos = models.ManyToManyField(
        Atributo, through="AtributoMonstro"
    )  # um monstro possui muitos atributos, um atributo está em diversos monstros.
    habilidades = models.ManyToManyField(
        Habilidade
    )  # um monstro possui muitas habilidades, uma habilidade está em diversos monstros.
    ataques = models.ManyToManyField(
        Ataque
    )  # um monstro possui muitos ataques, um ataque está em diversos monstros.
    pericias = models.ManyToManyField(
        Pericia, through="MonstroPericia", related_name="monstroPericia"
    )  # um monstro possui muitas pericias, uma pericia está em diversos monstros.

    def __str__(self):
        return self.nome

    def calcular_todas_pericias(self):
        pericias_valores = {}
        for pericia_treinada in self.periciatreinada_set.all():
            pericias_valores[pericia_treinada.pericia.nome] = (
                pericia_treinada.calcularValor()
            )
        return pericias_valores


# models relacionados a mesa de jogo
class Mesa(models.Model):
    dono = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    participante = models.ManyToManyField(
        User, through="MesaParticipante", related_name="mesa_participante"
    )
    nome = models.CharField(max_length=200, verbose_name="Nome da Mesa")
    descricao = models.TextField(
        verbose_name="Descrição da Mesa", null=True, blank=True
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )

    def __str__(self):
        return self.nome


class MesaParticipante(models.Model):
    tipo_participante = [("J", "Jogador"), ("M", "Mestre"), ("O", "Observador")]
    mesa = models.ForeignKey(
        Mesa, on_delete=models.CASCADE, related_name="mesa_jogador"
    )
    jogador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mesa_jogador"
    )
    tipo = models.CharField(
        max_length=1,
        choices=tipo_participante,
        default="Jogador",
        verbose_name="Tipo de Participante",
    )
    data_entrada = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Entrada"
    )
    data_saida = models.DateTimeField(
        null=True, blank=True, verbose_name="Data de Saída"
    )
    iniciativa = models.IntegerField(default=0, verbose_name="Iniciativa")
    ficha = models.ForeignKey(
        Ficha,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mesa_ficha",
    )

    def __str__(self):
        return f"{self.jogador.username} na mesa {self.mesa.nome}"


class MesaCombate(models.Model):
    mesa = models.ForeignKey(
        Mesa, on_delete=models.CASCADE, related_name="mesa_combate"
    )
    turno_atual = models.IntegerField(default=0, verbose_name="Turno Atual")
    monstros = models.ManyToManyField(
        Monstro, related_name="monstros_da_mesa", blank=True
    )

    def __str__(self):
        return f"Combate na mesa {self.mesa.nome} - Turno {self.turno_atual}"


# Padrão Composite para Itens
class Item(models.Model):
    """
    Classe base para itens usando padrão Composite.
    Pode ser um item simples ou um kit que contém outros itens.
    """

    nome = models.CharField(max_length=200, verbose_name="Nome do Item")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    peso = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.0, verbose_name="Peso (kg)"
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Valor (T$)"
    )

    # Indica se é um kit ou item
    eh_kit = models.BooleanField(default=False, verbose_name="É um Kit?")

    # Categoria do item
    CATEGORIA_CHOICES = [
        ("arma", "Arma"),
        ("armadura", "Armadura"),
        ("acessorio", "Acessório"),
        ("pocao", "Poção"),
        ("material", "Material"),
        ("kit", "Kit"),
        ("outros", "Outros"),
    ]
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default="outros",
        verbose_name="Categoria",
    )

    # Para kits: itens que este kit contém
    itens_do_kit = models.ManyToManyField(
        "self", through="ItemKit", symmetrical=False, blank=True
    )

    def __str__(self):
        prefixo = "Kit: " if self.eh_kit else ""
        return f"{prefixo}{self.nome}"

    def calcular_peso_total(self):
        """Calcula o peso total do item ou kit"""
        if not self.eh_kit:
            return self.peso

        # Para kits, soma o peso próprio + peso dos itens
        peso_total = self.peso
        for item_kit in self.itemkit_pai.all():
            peso_total += item_kit.item.calcular_peso_total() * item_kit.quantidade
        return peso_total

    def calcular_valor_total(self):
        """Calcula o valor total do item ou kit"""
        if not self.eh_kit:
            return self.valor

        # Para kits, soma o valor próprio + valor dos itens
        valor_total = self.valor
        for item_kit in self.itemkit_pai.all():
            valor_total += item_kit.item.calcular_valor_total() * item_kit.quantidade
        return valor_total

    def listar_itens(self):
        """Lista todos os itens (recursivamente se for kit)"""
        if not self.eh_kit:
            return [self]

        todos_itens = []
        for item_kit in self.itemkit_pai.all():
            for _ in range(item_kit.quantidade):
                todos_itens.extend(item_kit.item.listar_itens())
        return todos_itens


class ItemKit(models.Model):
    """
    Modelo intermediário para relacionar kits com itens.
    """

    kit = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemkit_pai")
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="itemkit_filho"
    )
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")

    class Meta:
        unique_together = ("kit", "item")
        verbose_name = "Item do Kit"
        verbose_name_plural = "Itens do Kit"

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} em {self.kit.nome}"


class InventarioFicha(models.Model):
    """
    Modelo para representar o inventário de uma ficha.
    Contém itens (simples ou kits) com quantidade.
    """

    ficha = models.ForeignKey(
        Ficha, on_delete=models.CASCADE, related_name="inventario"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    equipado = models.BooleanField(default=False, verbose_name="Equipado?")

    class Meta:
        verbose_name = "Item do Inventário"
        verbose_name_plural = "Itens do Inventário"
        unique_together = ("ficha", "item")  # Evita duplicatas

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} - {self.ficha.nome}"

    def calcular_peso_total(self):
        """Calcula o peso total considerando a quantidade"""
        return self.item.calcular_peso_total() * self.quantidade

    def calcular_valor_total(self):
        """Calcula o valor total considerando a quantidade"""
        return self.item.calcular_valor_total() * self.quantidade
