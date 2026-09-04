"""
Testes unitários para os serializers relacionados a Perícia:
- PericiaSerializer
- PericiaTreinadaSerializer
- PericiaTreinadaWriteSerializer
"""

from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import Pericia, PericiaTreinada, Ficha, Atributo, AtributoFicha
from backend.serializers import (
    PericiaSerializer,
    PericiaTreinadaSerializer,
    PericiaTreinadaWriteSerializer,
)


class PericiaSerializerTest(TestCase):
    # Suite de testes unitários para o PericiaSerializer. Testa a serialização e desserialização do modelo Pericia.

    def setUp(self):
        self.pericia_atletismo = Pericia.objects.create(nome="atl", requer_treino=False)
        self.pericia_ladinagem = Pericia.objects.create(nome="lad", requer_treino=True)

    def tearDown(self):
        Pericia.objects.all().delete()

    # --- Testes de Serialização (Model -> JSON) ---
    def test_serializacao_pericia_basica(self):
        serializer = PericiaSerializer(self.pericia_atletismo)
        data = serializer.data

        self.assertEqual(data["id"], self.pericia_atletismo.id)
        self.assertEqual(data["nome"], "atl")
        self.assertFalse(data["requer_treino"])

    def test_serializacao_pericia_com_treino_obrigatorio(self):
        serializer = PericiaSerializer(self.pericia_ladinagem)
        data = serializer.data

        self.assertEqual(data["nome"], "lad")
        self.assertTrue(data["requer_treino"])

    def test_serializacao_multiplas_pericias(self):
        pericias = Pericia.objects.all()
        serializer = PericiaSerializer(pericias, many=True)
        data = serializer.data

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["nome"], "atl")
        self.assertEqual(data[1]["nome"], "lad")

    # --- Testes de Desserialização (JSON -> Model) ---
    def test_desserializacao_pericia_valida(self):
        data = {"nome": "per", "requer_treino": False}
        serializer = PericiaSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia = serializer.save()

        self.assertEqual(pericia.nome, "per")
        self.assertFalse(pericia.requer_treino)

    def test_desserializacao_pericia_com_treino(self):
        data = {"nome": "gue", "requer_treino": True}
        serializer = PericiaSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia = serializer.save()

        self.assertEqual(pericia.nome, "gue")
        self.assertTrue(pericia.requer_treino)

    # --- Testes de Validação ---
    def test_validacao_nome_obrigatorio(self):
        data = {"requer_treino": False}
        serializer = PericiaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("nome", serializer.errors)

    def test_validacao_nome_invalido(self):
        data = {"nome": "xyz", "requer_treino": False}
        serializer = PericiaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("nome", serializer.errors)

    def test_validacao_requer_treino_default(self):
        # Testa se 'requer_treino' assume False quando não fornecido.
        data = {"nome": "cur"}
        serializer = PericiaSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia = serializer.save()
        self.assertFalse(pericia.requer_treino)

    # --- Testes de atualização ---
    def test_atualizacao_pericia(self):
        # Testa a atualização de uma perícia existente.
        data = {"nome": "atl", "requer_treino": True}
        serializer = PericiaSerializer(self.pericia_atletismo, data=data, partial=False)

        self.assertTrue(serializer.is_valid())
        pericia_atualizada = serializer.save()

        self.assertEqual(pericia_atualizada.nome, "atl")
        self.assertTrue(pericia_atualizada.requer_treino)

    def test_atualizacao_parcial_pericia(self):
        # Testa a atualização parcial (PATCH) de uma perícia.
        data = {"requer_treino": True}
        serializer = PericiaSerializer(self.pericia_atletismo, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        pericia_atualizada = serializer.save()

        self.assertEqual(pericia_atualizada.nome, "atl")  # Nome não muda
        self.assertTrue(pericia_atualizada.requer_treino)

    # --- Testes de campos ---
    def test_campos_incluidos_no_serializer(self):
        # Testa se todos os campos esperados estão incluídos no serializer.
        serializer = PericiaSerializer(self.pericia_atletismo)
        data = serializer.data

        campos_esperados = ["id", "nome", "requer_treino"]
        for campo in campos_esperados:
            self.assertIn(campo, data)

    def test_campos_read_only(self):
        # Testa se o campo 'id' é somente leitura.
        data = {
            "id": 999,  # Tenta definir ID manualmente
            "nome": "mis",
            "requer_treino": False,
        }
        serializer = PericiaSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia = serializer.save()

        # ID não deve ser 999
        self.assertNotEqual(pericia.id, 999)


class PericiaTreinadaSerializerTest(TestCase):
    # Suite de testes unitários para o PericiaTreinadaSerializer. Testa a serialização com campos relacionados e computados.

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        self.atributo_forca = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_destreza = Atributo.objects.create(nome="des", ordem=2)

        self.pericia_atletismo = Pericia.objects.create(nome="atl", requer_treino=False)
        self.pericia_ladinagem = Pericia.objects.create(nome="lad", requer_treino=True)

        self.ficha = Ficha.objects.create(
            dono=self.user, nome="Guerreiro Teste", nivel=10
        )

        self.atributo_forca_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_forca, ficha=self.ficha, valor=3  # +3 de modificador
        )

        self.pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=2,
        )
        self.pericia_treinada.atributo_chave.add(self.atributo_forca_ficha)

    def tearDown(self):
        PericiaTreinada.objects.all().delete()
        AtributoFicha.objects.all().delete()
        Ficha.objects.all().delete()
        Pericia.objects.all().delete()
        Atributo.objects.all().delete()
        User.objects.all().delete()

    # --- Testes de Serialização ---
    def test_serializacao_pericia_treinada_completa(self):
        # Testa a serialização completa de uma perícia treinada, incluindo campos relacionados e computados.
        serializer = PericiaTreinadaSerializer(self.pericia_treinada)
        data = serializer.data

        self.assertEqual(data["id"], self.pericia_treinada.id)
        self.assertTrue(data["treinado"])
        self.assertEqual(data["bonus_adicional"], 2)

        # Verifica perícia aninhada
        self.assertIn("pericia", data)
        self.assertEqual(data["pericia"]["nome"], "atl")

        # Verifica atributos chave aninhados
        self.assertIn("atributo_chave", data)
        self.assertEqual(len(data["atributo_chave"]), 1)
        self.assertEqual(data["atributo_chave"][0]["valor"], 3)

        # Verifica campo computado
        self.assertIn("valor_calculado", data)

    def test_calculo_valor_pericia_treinada(self):
        """
        Testa se o campo 'valor_calculado' retorna o valor correto.

        Fórmula: (nivel // 2) + atributo + bonus_treino + bonus_adicional
        Nível 10: (10 // 2) = 5
        Atributo: 3
        Bonus treino (nível 10): 4
        Bonus adicional: 2
        Total: 5 + 3 + 4 + 2 = 14
        """
        serializer = PericiaTreinadaSerializer(self.pericia_treinada)
        data = serializer.data

        valor_esperado = 14
        self.assertEqual(data["valor_calculado"], valor_esperado)

    def test_serializacao_pericia_nao_treinada(self):
        pericia_nao_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=0,
        )
        pericia_nao_treinada.atributo_chave.add(self.atributo_forca_ficha)

        serializer = PericiaTreinadaSerializer(pericia_nao_treinada)
        data = serializer.data

        self.assertFalse(data["treinado"])
        # (10 // 2) + 3 + 0 (sem treino) + 0 = 8
        self.assertEqual(data["valor_calculado"], 8)

    def test_serializacao_pericia_obrigatoria_sem_treino(self):
        pericia_sem_treino = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_ladinagem,  # Requer treino
            treinado=False,
            bonus_adicional=0,
        )
        pericia_sem_treino.atributo_chave.add(self.atributo_forca_ficha)

        serializer = PericiaTreinadaSerializer(pericia_sem_treino)
        data = serializer.data

        self.assertEqual(data["valor_calculado"], 0)

    def test_serializacao_multiplos_atributos(self):
        atributo_des_ficha = AtributoFicha.objects.create(
            atributo=self.atributo_destreza, ficha=self.ficha, valor=2
        )
        self.pericia_treinada.atributo_chave.add(atributo_des_ficha)

        serializer = PericiaTreinadaSerializer(self.pericia_treinada)
        data = serializer.data

        self.assertEqual(len(data["atributo_chave"]), 2)
        # (10 // 2) + (3 + 2) + 4 + 2 = 16
        self.assertEqual(data["valor_calculado"], 16)

    # --- Testes de campos aninhados ---
    def test_pericia_aninhada_campos(self):
        serializer = PericiaTreinadaSerializer(self.pericia_treinada)
        data = serializer.data

        pericia_data = data["pericia"]
        self.assertIn("id", pericia_data)
        self.assertIn("nome", pericia_data)
        self.assertIn("requer_treino", pericia_data)

    def test_atributo_chave_aninhado_campos(self):
        serializer = PericiaTreinadaSerializer(self.pericia_treinada)
        data = serializer.data

        atributo_data = data["atributo_chave"][0]
        self.assertIn("id", atributo_data)
        self.assertIn("atributo", atributo_data)
        self.assertIn("valor", atributo_data)

    # --- Testes de Read-Only ---
    def test_campos_read_only(self):
        # Testa se os campos nested são somente leitura. O PericiaTreinadaSerializer é usado apenas para leitura.
        serializer = PericiaTreinadaSerializer(self.pericia_treinada)

        # Verifica que os campos aninhados existem na serialização
        self.assertIn("pericia", serializer.data)
        self.assertIn("atributo_chave", serializer.data)
        self.assertIn("valor_calculado", serializer.data)


class PericiaTreinadaWriteSerializerTest(TestCase):
    # Suite de testes unitários para o PericiaTreinadaWriteSerializer. Testa a criação e atualização de perícias treinadas.
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        self.atributo_forca = Atributo.objects.create(nome="for", ordem=1)
        self.pericia_atletismo = Pericia.objects.create(nome="atl", requer_treino=False)

        self.ficha = Ficha.objects.create(
            dono=self.user, nome="Guerreiro Teste", nivel=5
        )

    def tearDown(self):
        PericiaTreinada.objects.all().delete()
        Ficha.objects.all().delete()
        Pericia.objects.all().delete()
        Atributo.objects.all().delete()
        User.objects.all().delete()

    # --- Testes de criação ---
    def test_criacao_pericia_treinada_valida(self):
        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            "treinado": True,
            "bonus_adicional": 5,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        pericia_treinada = serializer.save()

        self.assertEqual(pericia_treinada.ficha, self.ficha)
        self.assertEqual(pericia_treinada.pericia, self.pericia_atletismo)
        self.assertTrue(pericia_treinada.treinado)
        self.assertEqual(pericia_treinada.bonus_adicional, 5)

    def test_criacao_pericia_nao_treinada(self):
        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            "treinado": False,
            "bonus_adicional": 0,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia_treinada = serializer.save()

        self.assertFalse(pericia_treinada.treinado)
        self.assertEqual(pericia_treinada.bonus_adicional, 0)

    def test_criacao_com_bonus_negativo(self):
        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            "treinado": False,
            "bonus_adicional": -3,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia_treinada = serializer.save()

        self.assertEqual(pericia_treinada.bonus_adicional, -3)

    # --- Testes de validação ---
    def test_validacao_ficha_opcional(self):
        # Testa se o campo 'ficha' pode ser nulo (conforme definido no modelo).
        data = {
            "pericia": self.pericia_atletismo.id,
            "treinado": True,
            "bonus_adicional": 0,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        # O campo ficha permite null, então a validação deve passar
        self.assertTrue(serializer.is_valid(), serializer.errors)
        pericia_treinada = serializer.save()
        self.assertIsNone(pericia_treinada.ficha)

    def test_validacao_pericia_opcional(self):
        # Testa se o campo 'pericia' pode ser nulo (conforme definido no modelo).
        data = {"ficha": self.ficha.id, "treinado": True, "bonus_adicional": 0}
        serializer = PericiaTreinadaWriteSerializer(data=data)

        # O campo pericia permite null, então a validação deve passar
        self.assertTrue(serializer.is_valid(), serializer.errors)
        pericia_treinada = serializer.save()
        self.assertIsNone(pericia_treinada.pericia)

    def test_validacao_ficha_inexistente(self):
        # Testa se uma ficha inexistente é rejeitada.
        data = {
            "ficha": 99999,  # ID inexistente
            "pericia": self.pericia_atletismo.id,
            "treinado": True,
            "bonus_adicional": 0,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("ficha", serializer.errors)

    def test_validacao_pericia_inexistente(self):
        # Testa se uma perícia inexistente é rejeitada.
        data = {
            "ficha": self.ficha.id,
            "pericia": 99999,  # ID inexistente
            "treinado": True,
            "bonus_adicional": 0,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("pericia", serializer.errors)

    # --- Testes de atualização ---
    def test_atualizacao_pericia_treinada(self):
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=0,
        )

        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            "treinado": True,
            "bonus_adicional": 3,
        }
        serializer = PericiaTreinadaWriteSerializer(pericia_treinada, data=data)

        self.assertTrue(serializer.is_valid())
        pericia_atualizada = serializer.save()

        self.assertTrue(pericia_atualizada.treinado)
        self.assertEqual(pericia_atualizada.bonus_adicional, 3)

    def test_atualizacao_parcial(self):
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=2,
        )

        data = {"treinado": True}
        serializer = PericiaTreinadaWriteSerializer(
            pericia_treinada, data=data, partial=True
        )

        self.assertTrue(serializer.is_valid())
        pericia_atualizada = serializer.save()

        self.assertTrue(pericia_atualizada.treinado)
        self.assertEqual(pericia_atualizada.bonus_adicional, 2)  # Não muda

    # --- Testes de valores default ---
    def test_valores_default(self):
        # Testa se os valores padrão são aplicados quando não fornecidos.
        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            # treinado e bonus_adicional omitidos
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia_treinada = serializer.save()

        self.assertFalse(pericia_treinada.treinado)  # Default False
        self.assertEqual(pericia_treinada.bonus_adicional, 0)  # Default 0

    # --- Testes de campos write-only ---
    def test_ficha_write_only(self):
        pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )

        serializer = PericiaTreinadaWriteSerializer(pericia_treinada)
        data = serializer.data

        # O campo 'ficha' não deve aparecer na serialização
        # apenas 'id', 'pericia', 'treinado', 'bonus_adicional'
        self.assertIn("id", data)
        self.assertIn("pericia", data)
        self.assertIn("treinado", data)
        self.assertIn("bonus_adicional", data)

    # --- Testes de edge cases ---
    def test_bonus_adicional_muito_grande(self):
        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            "treinado": True,
            "bonus_adicional": 999999,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia_treinada = serializer.save()

        self.assertEqual(pericia_treinada.bonus_adicional, 999999)

    def test_bonus_adicional_muito_negativo(self):
        data = {
            "ficha": self.ficha.id,
            "pericia": self.pericia_atletismo.id,
            "treinado": True,
            "bonus_adicional": -999999,
        }
        serializer = PericiaTreinadaWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        pericia_treinada = serializer.save()

        self.assertEqual(pericia_treinada.bonus_adicional, -999999)
