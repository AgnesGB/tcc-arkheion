"""
Testes unitários para serializers básicos (Atributo, Pericia, Classe, etc.)
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
from backend.serializers import (
    AtributoSerializer,
    PericiaSerializer,
    ClasseSerializer,
    OrigemSerializer,
    RacaSerializer,
    DivindadeSerializer,
    HabilidadeSerializer,
    AtaqueSerializer,
)


class AtributoSerializerTest(TestCase):
    """Testes para AtributoSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.atributo = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_data = {"nome": "des", "ordem": 2}

    def test_serializer_com_instancia(self):
        """Testa serialização de instância existente"""
        serializer = AtributoSerializer(instance=self.atributo)
        data = serializer.data

        self.assertEqual(data["nome"], "for")
        self.assertEqual(data["ordem"], 1)
        self.assertIn("id", data)

    def test_serializer_com_dados(self):
        """Testa deserialização de dados"""
        serializer = AtributoSerializer(data=self.atributo_data)

        self.assertTrue(serializer.is_valid())
        atributo = serializer.save()

        self.assertEqual(atributo.nome, "des")
        self.assertEqual(atributo.ordem, 2)

    def test_serializer_campos_obrigatorios(self):
        """Testa validação de campos obrigatórios"""
        serializer = AtributoSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("nome", serializer.errors)


class PericiaSerializerTest(TestCase):
    """Testes para PericiaSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.pericia = Pericia.objects.create(nome="atl", requer_treino=False)

    def test_serializer_com_instancia(self):
        """Testa serialização de perícia"""
        serializer = PericiaSerializer(instance=self.pericia)
        data = serializer.data

        self.assertEqual(data["nome"], "atl")
        self.assertFalse(data["requer_treino"])

    def test_serializer_criar_pericia(self):
        """Testa criação via serializer"""
        data = {"nome": "fur", "requer_treino": True}
        serializer = PericiaSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia = serializer.save()

        self.assertEqual(pericia.nome, "fur")
        self.assertTrue(pericia.requer_treino)


class ClasseSerializerTest(TestCase):
    """Testes para ClasseSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.classe = Classe.objects.create(
            nome="Guerreiro",
            descricao="Mestre em combate",
            proficiencia="Armas marciais",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
            homebrew=False,
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de classe"""
        serializer = ClasseSerializer(instance=self.classe)
        data = serializer.data

        self.assertEqual(data["nome"], "Guerreiro")
        self.assertEqual(data["vida_base"], 20)
        self.assertEqual(data["vida_por_nivel"], 5)
        self.assertFalse(data["homebrew"])

    def test_serializer_criar_classe_magica(self):
        """Testa criação de classe com mana"""
        data = {
            "nome": "Mago",
            "descricao": "Mestre da magia",
            "proficiencia": "Cajados",
            "vida_base": 12,
            "vida_por_nivel": 3,
            "mana_base": 6,
            "mana_por_nivel": 6,
            "homebrew": False,
        }
        serializer = ClasseSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        classe = serializer.save()

        self.assertEqual(classe.mana_base, 6)
        self.assertEqual(classe.mana_por_nivel, 6)

    def test_serializer_todos_campos(self):
        """Testa que todos os campos estão presentes"""
        serializer = ClasseSerializer(instance=self.classe)
        expected_fields = [
            "id",
            "nome",
            "descricao",
            "proficiencia",
            "vida_base",
            "vida_por_nivel",
            "mana_base",
            "mana_por_nivel",
            "pericias_treinadas",
            "pericias_para_escolher",
            "homebrew",
        ]

        for field in expected_fields:
            self.assertIn(field, serializer.data)


class OrigemSerializerTest(TestCase):
    """Testes para OrigemSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.origem = Origem.objects.create(
            nome="Amnésico", descricao="Você não se lembra do passado", homebrew=False
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de origem"""
        serializer = OrigemSerializer(instance=self.origem)
        data = serializer.data

        self.assertEqual(data["nome"], "Amnésico")
        self.assertIsNotNone(data["descricao"])
        self.assertFalse(data["homebrew"])

    def test_serializer_campos_presentes(self):
        """Testa presença de todos os campos"""
        serializer = OrigemSerializer(instance=self.origem)
        expected_fields = ["id", "nome", "descricao", "homebrew"]

        for field in expected_fields:
            self.assertIn(field, serializer.data)


class RacaSerializerTest(TestCase):
    """Testes para RacaSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.raca = Raca.objects.create(
            nome="Humano", descricao="Versátil e adaptável", homebrew=False
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de raça"""
        serializer = RacaSerializer(instance=self.raca)
        data = serializer.data

        self.assertEqual(data["nome"], "Humano")
        self.assertEqual(data["descricao"], "Versátil e adaptável")
        self.assertFalse(data["homebrew"])

    def test_serializer_criar_raca(self):
        """Testa criação via serializer"""
        data = {"nome": "Elfo", "descricao": "Ágil e mágico", "homebrew": False}
        serializer = RacaSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        raca = serializer.save()

        self.assertEqual(raca.nome, "Elfo")


class DivindadeSerializerTest(TestCase):
    """Testes para DivindadeSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.divindade = Divindade.objects.create(
            nome="Khalmyr",
            descricao="Deus da Justiça",
            simbolo="Espada em chamas",
            obrigacoes="Proteger inocentes",
            restrições="Não tolerar injustiças",
            homebrew=False,
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de divindade"""
        serializer = DivindadeSerializer(instance=self.divindade)
        data = serializer.data

        self.assertEqual(data["nome"], "Khalmyr")
        self.assertEqual(data["simbolo"], "Espada em chamas")
        self.assertFalse(data["homebrew"])

    def test_serializer_campos_completos(self):
        """Testa todos os campos"""
        serializer = DivindadeSerializer(instance=self.divindade)
        expected_fields = [
            "id",
            "nome",
            "descricao",
            "obrigacoes",
            "restrições",
            "simbolo",
            "homebrew",
        ]

        for field in expected_fields:
            self.assertIn(field, serializer.data)


class HabilidadeSerializerTest(TestCase):
    """Testes para HabilidadeSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.raca = Raca.objects.create(nome="Elfo")
        self.classe = Classe.objects.create(
            nome="Ranger", proficiencia="Armas", vida_base=16, vida_por_nivel=4
        )
        self.origem = Origem.objects.create(nome="Caçador")

        self.habilidade_raca = Habilidade.objects.create(
            nome="Visão na Penumbra",
            descricao="Enxerga na escuridão",
            origem="rc",
            ativo=True,
            nivel_habilidade=0,
            raca_pers=self.raca,
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de habilidade"""
        serializer = HabilidadeSerializer(instance=self.habilidade_raca)
        data = serializer.data

        self.assertEqual(data["nome"], "Visão na Penumbra")
        self.assertEqual(data["origem"], "rc")
        self.assertTrue(data["ativo"])

    def test_serializer_origem_display(self):
        """Testa campo origem_display"""
        serializer = HabilidadeSerializer(instance=self.habilidade_raca)
        data = serializer.data

        self.assertIn("origem_display", data)
        self.assertEqual(data["origem_display"], "Raça")

    def test_serializer_relacionamentos_aninhados(self):
        """Testa serialização de relacionamentos"""
        serializer = HabilidadeSerializer(instance=self.habilidade_raca)
        data = serializer.data

        # Raça deve estar aninhada
        self.assertIn("raca_pers", data)
        self.assertIsNotNone(data["raca_pers"])
        self.assertEqual(data["raca_pers"]["nome"], "Elfo")

    def test_serializer_habilidade_classe(self):
        """Testa habilidade de classe"""
        hab_classe = Habilidade.objects.create(
            nome="Inimigo Favorito",
            descricao="Bônus contra inimigos",
            origem="cl",
            nivel_habilidade=1,
            classe_pers=self.classe,
        )

        serializer = HabilidadeSerializer(instance=hab_classe)
        data = serializer.data

        self.assertEqual(data["origem"], "cl")
        self.assertIsNotNone(data["classe_pers"])
        self.assertEqual(data["classe_pers"]["nome"], "Ranger")


class AtaqueSerializerTest(TestCase):
    """Testes para AtaqueSerializer"""

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

    def test_serializer_com_instancia(self):
        """Testa serialização de ataque"""
        serializer = AtaqueSerializer(instance=self.ataque)
        data = serializer.data

        self.assertEqual(data["nome"], "Espada Longa")
        self.assertEqual(data["dano"], "1d8")
        self.assertEqual(data["tipo_dano"], "cor")

    def test_serializer_tipo_dano_display(self):
        """Testa campo tipo_dano_display"""
        serializer = AtaqueSerializer(instance=self.ataque)
        data = serializer.data

        self.assertIn("tipo_dano_display", data)
        self.assertEqual(data["tipo_dano_display"], "Corte")

    def test_serializer_pericia_aninhada(self):
        """Testa serialização de perícia aninhada"""
        serializer = AtaqueSerializer(instance=self.ataque)
        data = serializer.data

        self.assertIn("pericia", data)
        self.assertIsNotNone(data["pericia"])
        self.assertEqual(data["pericia"]["nome"], "lut")

    def test_serializer_criar_ataque_magico(self):
        """Testa criação de ataque mágico"""
        data = {
            "nome": "Bola de Fogo",
            "descricao": "Explosão flamejante",
            "dano": "6d6",
            "tipo_dano": "fog",
            "resistencia": "Reflexos reduz à metade",
            "homebrew": False,
        }
        serializer = AtaqueSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        ataque = serializer.save()

        self.assertEqual(ataque.tipo_dano, "fog")
        self.assertEqual(ataque.dano, "6d6")
