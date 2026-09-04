"""
Testes de API para CDU014 - Utilizar Perícia
Baseado no planejamento em: doc/testes/CT-CDU014.md

Endpoints testados:
- POST /arkheion_api/fichas/{id}/update-pericia-treino/
- POST /arkheion_api/fichas/{id}/update-pericia-bonus/
- GET /arkheion_api/fichas/{id}/ (para visualizar perícias)
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from backend.models import Ficha, Pericia, AtributoFicha, Atributo, PericiaTreinada


class PericiaCalculoTestCase(TestCase):
    """
    Testes para cálculo de perícias (CDU014)
    """

    def setUp(self):
        """
        Configurar dados de teste antes de cada teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_user", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar ficha de teste
        self.ficha = Ficha.objects.create(
            dono=self.user, nome="Personagem Teste", nivel=10
        )

        # Criar atributos base
        self.atributo_forca = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_destreza = Atributo.objects.create(nome="des", ordem=2)
        self.atributo_constituicao = Atributo.objects.create(nome="con", ordem=3)
        self.atributo_inteligencia = Atributo.objects.create(nome="int", ordem=4)
        self.atributo_sabedoria = Atributo.objects.create(nome="sab", ordem=5)
        self.atributo_carisma = Atributo.objects.create(nome="car", ordem=6)

        # Criar AtributoFicha - Força 14 (+2 mod)
        self.attr_forca_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo_forca, valor=2  # Modificador +2
        )

        # Criar AtributoFicha - Destreza 16 (+3 mod)
        self.attr_destreza_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo_destreza, valor=3  # Modificador +3
        )

        # Criar AtributoFicha - Sabedoria 12 (+1 mod)
        self.attr_sabedoria_ficha = AtributoFicha.objects.create(
            ficha=self.ficha,
            atributo=self.atributo_sabedoria,
            valor=1,  # Modificador +1
        )

        # Criar perícias
        self.pericia_atletismo = Pericia.objects.create(nome="atl", requer_treino=False)

        self.pericia_ladinagem = Pericia.objects.create(nome="lad", requer_treino=True)

        self.pericia_percepcao = Pericia.objects.create(nome="per", requer_treino=False)

        # Criar PericiaTreinada para Atletismo
        self.pericia_treinada_atletismo = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_atletismo,
            treinado=False,
            bonus_adicional=0,
        )
        self.pericia_treinada_atletismo.atributo_chave.add(self.attr_forca_ficha)

        # Criar PericiaTreinada para Ladinagem (já treinada)
        self.pericia_treinada_ladinagem = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_ladinagem,
            treinado=True,
            bonus_adicional=0,
        )
        self.pericia_treinada_ladinagem.atributo_chave.add(self.attr_destreza_ficha)

        # Criar PericiaTreinada para Percepção
        self.pericia_treinada_percepcao = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=0,
        )
        self.pericia_treinada_percepcao.atributo_chave.add(self.attr_sabedoria_ficha)

    def test_calculo_pericia_comum_sem_treino(self):
        """
        Teste CT-PER-01: Cálculo de perícia comum (não requer treino)
        Atletismo (Não requer treino)
        Nível 10, Força 14 (+2 mod)
        Resultado: 5 (nível/2) + 2 (atributo) = 7
        """
        valor = self.pericia_treinada_atletismo.calcularValor()

        # CT-CDU014: 5 de nível (10/2) + 2 de atributo = 7
        self.assertEqual(valor, 7)

    def test_treino_nao_obrigatorio(self):
        """
        Teste CT-PER-02: Treino em perícia que não requer treino
        Atletismo marcada como treinada
        Nível 10 (bônus de treino = 4)
        Resultado: 7 (base) + 4 (treino) = 11
        """
        # Marcar como treinado
        self.pericia_treinada_atletismo.treinado = True
        self.pericia_treinada_atletismo.save()

        valor = self.pericia_treinada_atletismo.calcularValor()

        # CT-CDU014: 5 de nível + 2 de atributo + 4 de treino = 11
        self.assertEqual(valor, 11)

    def test_calculo_pericia_obrigatoria_com_treino(self):
        """
        Teste CT-PER-03: Cálculo de perícia que requer treino (já treinada)
        Ladinagem (Requer treino, já está treinada)

        Para testar este caso corretamente, vou criar uma nova ficha nível 4
        """
        # Criar ficha nível 4
        ficha_nivel_4 = Ficha.objects.create(
            dono=self.user, nome="Personagem Nível 4", nivel=4
        )

        # Criar AtributoFicha - Destreza 16 (+3 mod)
        attr_des_4 = AtributoFicha.objects.create(
            ficha=ficha_nivel_4, atributo=self.atributo_destreza, valor=3
        )

        # Criar PericiaTreinada para Ladinagem (treinada)
        pericia_lad_4 = PericiaTreinada.objects.create(
            ficha=ficha_nivel_4,
            pericia=self.pericia_ladinagem,
            treinado=True,
            bonus_adicional=0,
        )
        pericia_lad_4.atributo_chave.add(attr_des_4)

        valor = pericia_lad_4.calcularValor()

        # CT-CDU014: 2 (nível 4/2) + 3 (atributo) + 2 (treino nível 4) = 7
        self.assertEqual(valor, 7)

    def test_pericia_obrigatoria_sem_treino(self):
        """
        Teste CT-PER-04: Perícia que requer treino sem estar treinada
        Ladinagem desmarcada como treinada
        Resultado: 0 (perícia não pode ser usada)
        """
        # Desmarcar como treinado
        self.pericia_treinada_ladinagem.treinado = False
        self.pericia_treinada_ladinagem.save()

        valor = self.pericia_treinada_ladinagem.calcularValor()

        # CT-CDU014: Perícia obrigatória sem treino = 0
        self.assertEqual(valor, 0)

    def test_bonus_adicional_positivo(self):
        """
        Teste CT-PER-05: Inserir bônus adicional positivo
        Percepção com bônus adicional de +5

        Para testar este caso, vou criar uma ficha nível 8
        """
        # Criar ficha nível 8
        ficha_nivel_8 = Ficha.objects.create(
            dono=self.user, nome="Personagem Nível 8", nivel=8
        )

        # Criar AtributoFicha - Sabedoria 12 (+1 mod)
        attr_sab_8 = AtributoFicha.objects.create(
            ficha=ficha_nivel_8, atributo=self.atributo_sabedoria, valor=1
        )

        # Criar PericiaTreinada para Percepção
        pericia_per_8 = PericiaTreinada.objects.create(
            ficha=ficha_nivel_8,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=5,  # Bônus adicional de +5
        )
        pericia_per_8.atributo_chave.add(attr_sab_8)

        valor = pericia_per_8.calcularValor()

        # CT-CDU014: 4 (nível 8/2) + 1 (atributo) + 5 (bônus) = 10
        self.assertEqual(valor, 10)

    def test_bonus_adicional_negativo(self):
        """
        Teste CT-PER-06: Inserir bônus adicional negativo (penalidade)
        Percepção com bônus adicional de -2
        """
        # Criar ficha nível 8
        ficha_nivel_8 = Ficha.objects.create(
            dono=self.user, nome="Personagem Nível 8 Penalidade", nivel=8
        )

        # Criar AtributoFicha - Sabedoria 12 (+1 mod)
        attr_sab_8 = AtributoFicha.objects.create(
            ficha=ficha_nivel_8, atributo=self.atributo_sabedoria, valor=1
        )

        # Criar PericiaTreinada para Percepção
        pericia_per_8 = PericiaTreinada.objects.create(
            ficha=ficha_nivel_8,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=-2,  # Penalidade de -2
        )
        pericia_per_8.atributo_chave.add(attr_sab_8)

        valor = pericia_per_8.calcularValor()

        # CT-CDU014: 4 (nível 8/2) + 1 (atributo) - 2 (penalidade) = 3
        self.assertEqual(valor, 3)

    def test_bonus_adicional_zero(self):
        """
        Teste CT-PER-07: Bônus adicional igual a zero
        Sistema deve funcionar normalmente com bônus = 0
        """
        self.pericia_treinada_percepcao.bonus_adicional = 0
        self.pericia_treinada_percepcao.save()

        valor = self.pericia_treinada_percepcao.calcularValor()

        # Deve calcular normalmente: (10/2) + 1 = 6
        self.assertEqual(valor, 6)


class PericiaAPIEndpointTestCase(TestCase):
    """
    Testes para os endpoints de API de perícias
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_user_api", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar ficha
        self.ficha = Ficha.objects.create(
            dono=self.user, nome="Ficha API Test", nivel=8
        )

        # Criar atributos
        self.atributo_sabedoria = Atributo.objects.create(nome="sab", ordem=5)
        self.attr_sab_ficha = AtributoFicha.objects.create(
            ficha=self.ficha, atributo=self.atributo_sabedoria, valor=1
        )

        # Criar perícia
        self.pericia_percepcao = Pericia.objects.create(nome="per", requer_treino=False)

        # Criar PericiaTreinada
        self.pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha,
            pericia=self.pericia_percepcao,
            treinado=False,
            bonus_adicional=0,
        )
        self.pericia_treinada.atributo_chave.add(self.attr_sab_ficha)

        self.url_update_bonus = (
            f"/arkheion_api/personagem/{self.ficha.id}/update-pericia-bonus/"
        )
        self.url_update_treino = (
            f"/arkheion_api/personagem/{self.ficha.id}/update-pericia-treino/"
        )

    def test_api_atualizar_bonus_adicional_valido(self):
        """
        Teste CT-PER-05 API: Atualizar bônus adicional via API com valor válido
        """
        payload = {"pericia_id": self.pericia_percepcao.id, "bonus_adicional": 5}

        response = self.client.post(self.url_update_bonus, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        # Valor esperado: 4 (nível/2) + 1 (atributo) + 5 (bônus) = 10
        self.assertEqual(response.data["valor"], 10)

        # Verificar que foi salvo no banco
        self.pericia_treinada.refresh_from_db()
        self.assertEqual(self.pericia_treinada.bonus_adicional, 5)

    def test_api_atualizar_bonus_adicional_negativo(self):
        """
        Teste CT-PER-06 API: Atualizar bônus adicional com valor negativo
        """
        payload = {"pericia_id": self.pericia_percepcao.id, "bonus_adicional": -2}

        response = self.client.post(self.url_update_bonus, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Valor esperado: 4 (nível/2) + 1 (atributo) - 2 (penalidade) = 3
        self.assertEqual(response.data["valor"], 3)

    def test_api_atualizar_bonus_invalido(self):
        """
        Teste CT-PER-08 API: Tentar atualizar bônus com valor inválido (não numérico)
        """
        payload = {"pericia_id": self.pericia_percepcao.id, "bonus_adicional": "abc"}

        response = self.client.post(self.url_update_bonus, payload, format="json")

        # API deve retornar erro
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("número inteiro", str(response.data).lower())

    def test_api_atualizar_treino_marcar(self):
        """
        Teste CT-PER-02 API: Marcar perícia como treinada via API
        """
        payload = {"pericia_id": self.pericia_percepcao.id, "treinado": True}

        response = self.client.post(self.url_update_treino, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")

        # Verificar que foi salvo
        self.pericia_treinada.refresh_from_db()
        self.assertTrue(self.pericia_treinada.treinado)

    def test_api_atualizar_treino_desmarcar(self):
        """
        Teste CT-PER-04 API: Desmarcar perícia como treinada via API
        """
        # Primeiro marcar como treinada
        self.pericia_treinada.treinado = True
        self.pericia_treinada.save()

        payload = {"pericia_id": self.pericia_percepcao.id, "treinado": False}

        response = self.client.post(self.url_update_treino, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que foi desmarcado
        self.pericia_treinada.refresh_from_db()
        self.assertFalse(self.pericia_treinada.treinado)

    def test_api_campos_obrigatorios_bonus(self):
        """
        Teste adicional: Verificar validação de campos obrigatórios para bônus
        """
        # Sem pericia_id
        payload = {"bonus_adicional": 5}

        response = self.client.post(self.url_update_bonus, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Sem bonus_adicional
        payload = {"pericia_id": self.pericia_percepcao.id}

        response = self.client.post(self.url_update_bonus, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_campos_obrigatorios_treino(self):
        """
        Teste adicional: Verificar validação de campos obrigatórios para treino
        """
        # Sem pericia_id
        payload = {"treinado": True}

        response = self.client.post(self.url_update_treino, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Sem treinado
        payload = {"pericia_id": self.pericia_percepcao.id}

        response = self.client.post(self.url_update_treino, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_pericia_inexistente(self):
        """
        Teste adicional: Tentar atualizar perícia que não existe
        """
        payload = {"pericia_id": 99999, "bonus_adicional": 5}  # ID inexistente

        response = self.client.post(self.url_update_bonus, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_sem_autenticacao(self):
        """
        Teste adicional: Tentar atualizar perícia sem autenticação
        """
        # Remover credenciais
        self.client.credentials()

        payload = {"pericia_id": self.pericia_percepcao.id, "bonus_adicional": 5}

        response = self.client.post(self.url_update_bonus, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_visualizar_pericias_na_ficha(self):
        """
        Teste adicional: Verificar que perícias são retornadas ao buscar ficha
        """
        url_ficha = f"/arkheion_api/personagem/{self.ficha.id}/"
        response = self.client.get(url_ficha)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pericias_treinadas", response.data)

        # Verificar que a perícia está na lista
        pericias = response.data["pericias_treinadas"]
        self.assertTrue(len(pericias) > 0)

        # Encontrar a perícia de percepção
        pericia_per = next((p for p in pericias if p["pericia"]["nome"] == "per"), None)
        self.assertIsNotNone(pericia_per)
        self.assertIn("valor_calculado", pericia_per)


class PericiaBonusTreinoTestCase(TestCase):
    """
    Testes específicos para bônus de treino em diferentes níveis
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.user = User.objects.create_user(username="test_bonus", password="testpass")

        # Criar atributos
        self.atributo_forca = Atributo.objects.create(nome="for", ordem=1)

        # Criar perícia
        self.pericia_atletismo = Pericia.objects.create(nome="atl", requer_treino=False)

    def test_bonus_treino_nivel_0_a_5(self):
        """
        Teste: Bônus de treino para nível 0-5 deve ser +2
        """
        ficha = Ficha.objects.create(dono=self.user, nome="Nível 3", nivel=3)

        attr_ficha = AtributoFicha.objects.create(
            ficha=ficha, atributo=self.atributo_forca, valor=2
        )

        pericia = PericiaTreinada.objects.create(
            ficha=ficha,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia.atributo_chave.add(attr_ficha)

        bonus_treino = pericia.verificarTreino()
        self.assertEqual(bonus_treino, 2)

    def test_bonus_treino_nivel_6_a_14(self):
        """
        Teste: Bônus de treino para nível 6-14 deve ser +4
        """
        ficha = Ficha.objects.create(dono=self.user, nome="Nível 10", nivel=10)

        attr_ficha = AtributoFicha.objects.create(
            ficha=ficha, atributo=self.atributo_forca, valor=2
        )

        pericia = PericiaTreinada.objects.create(
            ficha=ficha,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia.atributo_chave.add(attr_ficha)

        bonus_treino = pericia.verificarTreino()
        self.assertEqual(bonus_treino, 4)

    def test_bonus_treino_nivel_15_ou_mais(self):
        """
        Teste: Bônus de treino para nível 15+ deve ser +6
        """
        ficha = Ficha.objects.create(dono=self.user, nome="Nível 20", nivel=20)

        attr_ficha = AtributoFicha.objects.create(
            ficha=ficha, atributo=self.atributo_forca, valor=2
        )

        pericia = PericiaTreinada.objects.create(
            ficha=ficha,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        pericia.atributo_chave.add(attr_ficha)

        bonus_treino = pericia.verificarTreino()
        self.assertEqual(bonus_treino, 6)

    def test_bonus_treino_sem_treino(self):
        """
        Teste: Sem treino, bônus deve ser 0
        """
        ficha = Ficha.objects.create(dono=self.user, nome="Sem Treino", nivel=10)

        attr_ficha = AtributoFicha.objects.create(
            ficha=ficha, atributo=self.atributo_forca, valor=2
        )

        pericia = PericiaTreinada.objects.create(
            ficha=ficha,
            pericia=self.pericia_atletismo,
            treinado=False,  # Não treinado
            bonus_adicional=0,
        )
        pericia.atributo_chave.add(attr_ficha)

        bonus_treino = pericia.verificarTreino()
        self.assertEqual(bonus_treino, 0)
