"""
Testes unitários para models básicos (Atributo, Pericia, Classe, Origem, Raça, Divindade)
"""

from django.test import TestCase
from backend.models import (
    Atributo,
    Pericia,
    Classe,
    Origem,
    Raca,
    Divindade,
    Habilidade,
    Ataque,
)


class AtributoModelTest(TestCase):
    """Testes para o model Atributo"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.atributo = Atributo.objects.create(nome="for", ordem=1)

    def test_criacao_atributo(self):
        """Testa se o atributo é criado corretamente"""
        self.assertEqual(self.atributo.nome, "for")
        self.assertEqual(self.atributo.ordem, 1)

    def test_str_atributo(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.atributo), "Força")

    def test_get_nome_display(self):
        """Testa se o display name está correto"""
        self.assertEqual(self.atributo.get_nome_display(), "Força")

    def test_todos_atributos_validos(self):
        """Testa a criação de todos os atributos válidos"""
        atributos_validos = ["for", "des", "con", "int", "sab", "car"]
        for atrib in atributos_validos:
            obj = Atributo.objects.create(nome=atrib, ordem=1)
            self.assertIsNotNone(obj.pk)


class PericiaModelTest(TestCase):
    """Testes para o model Pericia"""

    def setUp(self):
        """Configuração inicial"""
        self.pericia = Pericia.objects.create(nome="atl", requer_treino=False)
        self.pericia_treino = Pericia.objects.create(nome="gue", requer_treino=True)

    def test_criacao_pericia(self):
        """Testa criação de perícia"""
        self.assertEqual(self.pericia.nome, "atl")
        self.assertFalse(self.pericia.requer_treino)

    def test_pericia_requer_treino(self):
        """Testa perícia que requer treino"""
        self.assertTrue(self.pericia_treino.requer_treino)

    def test_str_pericia(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.pericia), "Atletismo")

    def test_default_requer_treino(self):
        """Testa valor padrão de requer_treino"""
        pericia_nova = Pericia.objects.create(nome="per")
        self.assertFalse(pericia_nova.requer_treino)


class ClasseModelTest(TestCase):
    """Testes para o model Classe"""

    def setUp(self):
        """Configuração inicial"""
        self.classe = Classe.objects.create(
            nome="Guerreiro",
            descricao="Mestre em combate",
            proficiencia="Armas marciais, armaduras pesadas",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
            pericias_treinadas="Atletismo, Luta",
            pericias_para_escolher="Fortitude, Intimidação",
            homebrew=False,
        )

    def test_criacao_classe(self):
        """Testa criação de classe"""
        self.assertEqual(self.classe.nome, "Guerreiro")
        self.assertEqual(self.classe.vida_base, 20)
        self.assertEqual(self.classe.vida_por_nivel, 5)

    def test_str_classe(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.classe), "Guerreiro")

    def test_classe_magica(self):
        """Testa criação de classe com mana"""
        mago = Classe.objects.create(
            nome="Mago",
            descricao="Mestre da magia",
            proficiencia="Bastões, cajados",
            vida_base=12,
            vida_por_nivel=3,
            mana_base=6,
            mana_por_nivel=6,
            homebrew=False,
        )
        self.assertEqual(mago.mana_base, 6)
        self.assertEqual(mago.mana_por_nivel, 6)

    def test_default_homebrew(self):
        """Testa valor padrão de homebrew"""
        self.assertFalse(self.classe.homebrew)


class OrigemModelTest(TestCase):
    """Testes para o model Origem"""

    def setUp(self):
        """Configuração inicial"""
        self.origem = Origem.objects.create(
            nome="Amnésico",
            descricao="Você não se lembra do seu passado",
            homebrew=False,
        )

    def test_criacao_origem(self):
        """Testa criação de origem"""
        self.assertEqual(self.origem.nome, "Amnésico")
        self.assertIsNotNone(self.origem.descricao)

    def test_str_origem(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.origem), "Amnésico")

    def test_origem_homebrew(self):
        """Testa criação de origem homebrew"""
        origem_hb = Origem.objects.create(nome="Origem Custom", homebrew=True)
        self.assertTrue(origem_hb.homebrew)


class RacaModelTest(TestCase):
    """Testes para o model Raca"""

    def setUp(self):
        """Configuração inicial"""
        self.raca = Raca.objects.create(
            nome="Humano", descricao="Versátil e adaptável", homebrew=False
        )

    def test_criacao_raca(self):
        """Testa criação de raça"""
        self.assertEqual(self.raca.nome, "Humano")
        self.assertIsNotNone(self.raca.descricao)

    def test_str_raca(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.raca), "Humano")

    def test_raca_homebrew(self):
        """Testa criação de raça homebrew"""
        raca_hb = Raca.objects.create(nome="Raça Custom", homebrew=True)
        self.assertTrue(raca_hb.homebrew)


class DivindadeModelTest(TestCase):
    """Testes para o model Divindade"""

    def setUp(self):
        """Configuração inicial"""
        self.divindade = Divindade.objects.create(
            nome="Khalmyr",
            descricao="Deus da Justiça",
            simbolo="Espada em chamas",
            obrigacoes="Proteger os inocentes",
            restrições="Não tolerar injustiças",
            homebrew=False,
        )

    def test_criacao_divindade(self):
        """Testa criação de divindade"""
        self.assertEqual(self.divindade.nome, "Khalmyr")
        self.assertEqual(self.divindade.simbolo, "Espada em chamas")

    def test_str_divindade(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.divindade), "Khalmyr")

    def test_divindade_sem_simbolo(self):
        """Testa criação de divindade sem símbolo"""
        div = Divindade.objects.create(nome="Divindade Teste", homebrew=True)
        self.assertIsNone(div.simbolo)


class HabilidadeModelTest(TestCase):
    """Testes para o model Habilidade"""

    def setUp(self):
        """Configuração inicial"""
        self.raca = Raca.objects.create(nome="Elfo")
        self.classe = Classe.objects.create(
            nome="Ranger", proficiencia="Armas", vida_base=16, vida_por_nivel=4
        )

        self.habilidade_raca = Habilidade.objects.create(
            nome="Visão na Penumbra",
            descricao="Enxerga na escuridão",
            origem="rc",
            ativo=True,
            nivel_habilidade=0,
            raca_pers=self.raca,
            homebrew=False,
        )

    def test_criacao_habilidade(self):
        """Testa criação de habilidade"""
        self.assertEqual(self.habilidade_raca.nome, "Visão na Penumbra")
        self.assertEqual(self.habilidade_raca.origem, "rc")

    def test_str_habilidade(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.habilidade_raca), "Visão na Penumbra")

    def test_habilidade_classe(self):
        """Testa habilidade de classe"""
        hab_classe = Habilidade.objects.create(
            nome="Inimigo Favorito",
            descricao="Bônus contra inimigos",
            origem="cl",
            nivel_habilidade=1,
            classe_pers=self.classe,
        )
        self.assertEqual(hab_classe.classe_pers, self.classe)

    def test_habilidade_ativa(self):
        """Testa habilidade ativa/passiva"""
        self.assertTrue(self.habilidade_raca.ativo)


class AtaqueModelTest(TestCase):
    """Testes para o model Ataque"""

    def setUp(self):
        """Configuração inicial"""
        self.pericia = Pericia.objects.create(nome="lut")
        self.ataque = Ataque.objects.create(
            nome="Espada Longa",
            descricao="Ataque com espada",
            dano="1d8",
            tipo_dano="cor",
            pericia=self.pericia,
            resistencia="---",
            homebrew=False,
        )

    def test_criacao_ataque(self):
        """Testa criação de ataque"""
        self.assertEqual(self.ataque.nome, "Espada Longa")
        self.assertEqual(self.ataque.dano, "1d8")
        self.assertEqual(self.ataque.tipo_dano, "cor")

    def test_str_ataque(self):
        """Testa o método __str__"""
        self.assertEqual(str(self.ataque), "Espada Longa")

    def test_ataque_magico(self):
        """Testa criação de ataque mágico"""
        ataque_mag = Ataque.objects.create(
            nome="Bola de Fogo",
            descricao="Explosão flamejante",
            dano="6d6",
            tipo_dano="fog",
            resistencia="Reflexos reduz à metade",
        )
        self.assertEqual(ataque_mag.tipo_dano, "fog")

    def test_default_resistencia(self):
        """Testa valor padrão de resistência"""
        self.assertEqual(self.ataque.resistencia, "---")
