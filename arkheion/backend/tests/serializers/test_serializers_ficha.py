"""
Testes unitários para serializers relacionados a Ficha
"""

from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import (
    Ficha,
    AtributoFicha,
    Atributo,
    PericiaTreinada,
    Pericia,
    NivelClasseFicha,
    Classe,
)
from backend.serializers import (
    FichaSerializer,
    AtributoFichaSerializer,
    PericiaTreinadaSerializer,
    NivelClasseFichaSerializer,
    AtributoFichaWriteSerializer,
)


class AtributoFichaSerializerTest(TestCase):
    """Testes para AtributoFichaSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Herói", dono=self.user)
        self.atributo = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo, valor=3
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de atributo da ficha"""
        serializer = AtributoFichaSerializer(instance=self.atributo_ficha)
        data = serializer.data

        self.assertEqual(data["valor"], 3)
        self.assertIn("atributo", data)
        self.assertIsNotNone(data["atributo"])

    def test_serializer_atributo_aninhado(self):
        """Testa que atributo está aninhado"""
        serializer = AtributoFichaSerializer(instance=self.atributo_ficha)
        data = serializer.data

        self.assertIn("nome", data["atributo"])
        self.assertEqual(data["atributo"]["nome"], "for")


class AtributoFichaWriteSerializerTest(TestCase):
    """Testes para AtributoFichaWriteSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Herói", dono=self.user)
        self.atributo = Atributo.objects.create(nome="des", ordem=2)

    def test_serializer_criar_atributo_ficha(self):
        """Testa criação via write serializer"""
        data = {"ficha": self.ficha.id, "atributo": self.atributo.id, "valor": 4}
        serializer = AtributoFichaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        atributo_ficha = serializer.save()

        self.assertEqual(atributo_ficha.valor, 4)
        self.assertEqual(atributo_ficha.ficha, self.ficha)


class PericiaTreinadaSerializerTest(TestCase):
    """Testes para PericiaTreinadaSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Teste", nivel=5, dono=self.user)
        self.pericia = Pericia.objects.create(nome="atl")
        self.atributo = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo, valor=3
        )

        self.pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha, pericia=self.pericia, treinado=True, bonus_adicional=2
        )
        self.pericia_treinada.atributo_chave.add(self.atributo_ficha)

    def test_serializer_com_instancia(self):
        """Testa serialização de perícia treinada"""
        serializer = PericiaTreinadaSerializer(instance=self.pericia_treinada)
        data = serializer.data

        self.assertTrue(data["treinado"])
        self.assertEqual(data["bonus_adicional"], 2)

    def test_serializer_valor_calculado(self):
        """Testa campo calculado valor_calculado"""
        serializer = PericiaTreinadaSerializer(instance=self.pericia_treinada)
        data = serializer.data

        self.assertIn("valor_calculado", data)
        # (nivel // 2) + valor_atributo + bonus_treino + bonus_adicional
        # (5 // 2) + 3 + 2 + 2 = 9
        self.assertEqual(data["valor_calculado"], 9)

    def test_serializer_pericia_aninhada(self):
        """Testa que perícia está aninhada"""
        serializer = PericiaTreinadaSerializer(instance=self.pericia_treinada)
        data = serializer.data

        self.assertIn("pericia", data)
        self.assertEqual(data["pericia"]["nome"], "atl")

    def test_serializer_atributos_chave_aninhados(self):
        """Testa que atributos chave estão aninhados"""
        serializer = PericiaTreinadaSerializer(instance=self.pericia_treinada)
        data = serializer.data

        self.assertIn("atributo_chave", data)
        self.assertIsInstance(data["atributo_chave"], list)
        self.assertEqual(len(data["atributo_chave"]), 1)


class NivelClasseFichaSerializerTest(TestCase):
    """Testes para NivelClasseFichaSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.ficha = Ficha.objects.create(nome="Teste", dono=self.user)
        self.classe = Classe.objects.create(
            nome="Guerreiro", proficiencia="Armas", vida_base=20, vida_por_nivel=5
        )
        self.nivel_classe = NivelClasseFicha.objects.create(
            ficha=self.ficha, classe=self.classe, nivel=5
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de nível de classe"""
        serializer = NivelClasseFichaSerializer(instance=self.nivel_classe)
        data = serializer.data

        self.assertEqual(data["nivel"], 5)
        self.assertIn("classe", data)

    def test_serializer_classe_aninhada(self):
        """Testa que classe está aninhada"""
        serializer = NivelClasseFichaSerializer(instance=self.nivel_classe)
        data = serializer.data

        self.assertIsNotNone(data["classe"])
        self.assertEqual(data["classe"]["nome"], "Guerreiro")
        self.assertEqual(data["classe"]["vida_base"], 20)


class FichaSerializerTest(TestCase):
    """Testes para FichaSerializer (serializer principal)"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username="test", password="pass")
        self.classe = Classe.objects.create(
            nome="Guerreiro",
            proficiencia="Armas",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
        )

        self.ficha = Ficha.objects.create(
            dono=self.user,
            nome="Conan",
            nivel=5,
            cd="15",
            ca="18",
            vida_atual=50,
            mana_atual=0,
        )

    def test_serializer_com_instancia_basica(self):
        """Testa serialização básica de ficha"""
        serializer = FichaSerializer(instance=self.ficha)
        data = serializer.data

        self.assertEqual(data["nome"], "Conan")
        self.assertEqual(data["nivel"], 5)
        self.assertEqual(data["cd"], "15")
        self.assertEqual(data["ca"], "18")

    def test_serializer_campos_read_only(self):
        """Testa que campos read_only estão presentes"""
        FichaSerializer(instance=self.ficha)

        # Verificar que os campos read_only existem no Meta
        self.assertIn("dono", FichaSerializer.Meta.read_only_fields)
        self.assertIn("nivel", FichaSerializer.Meta.read_only_fields)

    def test_serializer_relacionamentos_aninhados(self):
        """Testa que relacionamentos aparecem aninhados"""
        # Adicionar atributo
        atributo = Atributo.objects.create(nome="for", ordem=1)
        AtributoFicha.objects.create(ficha=self.ficha, atributo=atributo, valor=3)

        # Adicionar classe
        NivelClasseFicha.objects.create(ficha=self.ficha, classe=self.classe, nivel=5)

        serializer = FichaSerializer(instance=self.ficha)
        data = serializer.data

        # Verificar relacionamentos aninhados
        self.assertIn("atributos_ficha", data)
        self.assertIn("niveis_classes", data)
        self.assertIsInstance(data["atributos_ficha"], list)
        self.assertIsInstance(data["niveis_classes"], list)

    def test_serializer_criar_ficha_simples(self):
        """Testa criação de ficha via serializer"""
        data = {
            "nome": "Nova Ficha",
            "cd": "12",
            "ca": "15",
            "deslocamento": "9 metros",
            "tamanho": "Médio",
        }
        serializer = FichaSerializer(data=data)
        serializer.context["request"] = type("Request", (), {"user": self.user})()

        self.assertTrue(serializer.is_valid(), serializer.errors)
        ficha = serializer.save(dono=self.user)

        self.assertEqual(ficha.nome, "Nova Ficha")
        self.assertEqual(ficha.dono, self.user)

    def test_serializer_todos_campos_presentes(self):
        """Testa que usa __all__ nos fields"""
        serializer = FichaSerializer(instance=self.ficha)

        # Campos importantes devem estar presentes
        expected_fields = [
            "id",
            "nome",
            "nivel",
            "cd",
            "ca",
            "vida_atual",
            "mana_atual",
        ]
        for field in expected_fields:
            self.assertIn(field, serializer.data)
