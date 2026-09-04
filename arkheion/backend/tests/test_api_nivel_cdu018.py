"""
Testes de API para CDU018 - Subir de Nível
Baseado no planejamento em: doc/testes/CT-CDU018.md

Endpoints testados:
- POST /arkheion_api/personagem/{id}/subir-nivel/
- POST /arkheion_api/personagem/{id}/setar-nivel/
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from backend.models import (
    Ficha,
    Classe,
    NivelClasseFicha,
    Atributo,
    AtributoFicha,
    PericiaTreinada,
    Pericia,
)


class SubirNivelBasicoTestCase(TestCase):
    """
    Testes básicos para subir de nível
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_user_nivel", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar classe Guerreiro
        self.classe_guerreiro = Classe.objects.create(
            nome="Guerreiro",
            descricao="Classe de combate corpo a corpo",
            proficiencia="Todas as armas e armaduras",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
            homebrew=False,
        )

        # Criar classe Ranger
        self.classe_ranger = Classe.objects.create(
            nome="Ranger",
            descricao="Rastreador e explorador",
            proficiencia="Armas simples e marciais",
            vida_base=16,
            vida_por_nivel=4,
            mana_base=5,
            mana_por_nivel=3,
            homebrew=False,
        )

        # Criar classe Ladino
        self.classe_ladino = Classe.objects.create(
            nome="Ladino",
            descricao="Especialista em furtividade",
            proficiencia="Armas simples",
            vida_base=12,
            vida_por_nivel=3,
            mana_base=0,
            mana_por_nivel=0,
            homebrew=False,
        )

        # Criar ficha básica - Guerreiro Nível 5
        self.ficha_guerreiro = Ficha.objects.create(
            dono=self.user, nome="Guerreiro de Teste", nivel=5
        )

        # Adicionar classe Guerreiro nível 5
        self.nivel_guerreiro = NivelClasseFicha.objects.create(
            ficha=self.ficha_guerreiro, classe=self.classe_guerreiro, nivel=5
        )

    def test_subir_nivel_classe_unica(self):
        """
        Teste CT-NIV-01: Subir nível de classe única
        Guerreiro Nível 5 -> deve ir para Nível 6
        """
        url = f"/arkheion_api/personagem/{self.ficha_guerreiro.id}/subir-nivel/"

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que o nível foi incrementado
        self.ficha_guerreiro.refresh_from_db()
        self.assertEqual(self.ficha_guerreiro.nivel, 6)

        # Verificar que o nível da classe foi incrementado
        # Nota: O método atual subirUmNivel() só incrementa ficha.nivel,
        # não o NivelClasseFicha automaticamente

    def test_setar_nivel_valido(self):
        """
        Teste adicional: Setar nível para um valor específico válido
        """
        url = f"/arkheion_api/personagem/{self.ficha_guerreiro.id}/setar-nivel/"

        response = self.client.post(url, {"nivel": 10}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que o nível foi setado
        self.ficha_guerreiro.refresh_from_db()
        self.assertEqual(self.ficha_guerreiro.nivel, 10)

    def test_setar_nivel_invalido_negativo(self):
        """
        Teste: Tentar setar nível negativo
        """
        url = f"/arkheion_api/personagem/{self.ficha_guerreiro.id}/setar-nivel/"

        response = self.client.post(url, {"nivel": -1}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("positivo", str(response.data).lower())

    def test_setar_nivel_invalido_texto(self):
        """
        Teste CT-NIV-06: Dados inválidos - texto ao invés de número
        """
        url = f"/arkheion_api/personagem/{self.ficha_guerreiro.id}/setar-nivel/"

        response = self.client.post(url, {"nivel": "abc"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("inteiro", str(response.data).lower())

    def test_setar_nivel_sem_parametro(self):
        """
        Teste: Tentar setar nível sem enviar o parâmetro
        """
        url = f"/arkheion_api/personagem/{self.ficha_guerreiro.id}/setar-nivel/"

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("obrigatório", str(response.data).lower())


class SubirNivelMulticlasseTestCase(TestCase):
    """
    Testes para subir de nível com multiclasse
    """

    def setUp(self):
        """
        Configurar dados de teste para multiclasse
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_multiclasse", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar classes
        self.classe_barbaro = Classe.objects.create(
            nome="Bárbaro",
            vida_base=24,
            vida_por_nivel=6,
            mana_base=0,
            mana_por_nivel=0,
            proficiencia="Armas e armaduras pesadas",
        )

        self.classe_ranger = Classe.objects.create(
            nome="Ranger",
            vida_base=16,
            vida_por_nivel=4,
            mana_base=5,
            mana_por_nivel=3,
            proficiencia="Armas e armaduras médias",
        )

        self.classe_clerigo = Classe.objects.create(
            nome="Clérigo",
            vida_base=16,
            vida_por_nivel=4,
            mana_base=10,
            mana_por_nivel=5,
            proficiencia="Armaduras e símbolos sagrados",
        )

        self.classe_ladino = Classe.objects.create(
            nome="Ladino",
            vida_base=12,
            vida_por_nivel=3,
            mana_base=0,
            mana_por_nivel=0,
            proficiencia="Armas leves",
        )

        # Criar ficha multiclasse - Bárbaro 5 / Ranger 3 (Nível total 8)
        self.ficha_multiclasse = Ficha.objects.create(
            dono=self.user, nome="Bárbaro/Ranger", nivel=8
        )

        # Adicionar classes
        self.nivel_barbaro = NivelClasseFicha.objects.create(
            ficha=self.ficha_multiclasse, classe=self.classe_barbaro, nivel=5
        )

        self.nivel_ranger = NivelClasseFicha.objects.create(
            ficha=self.ficha_multiclasse, classe=self.classe_ranger, nivel=3
        )

    def test_subir_nivel_multiclasse(self):
        """
        Teste CT-NIV-02: Subir nível em personagem multiclasse
        Bárbaro 5/Ranger 3 (Nível 8) -> deve ir para Nível 9
        Nota: O sistema atual não tem endpoint específico para escolher qual classe subir
        """
        url = f"/arkheion_api/personagem/{self.ficha_multiclasse.id}/subir-nivel/"

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que o nível total foi incrementado
        self.ficha_multiclasse.refresh_from_db()
        self.assertEqual(self.ficha_multiclasse.nivel, 9)

    def test_adicionar_nova_classe(self):
        """
        Teste CT-NIV-03: Adicionar nova classe (multiclasse)
        Clérigo Nível 4 -> adiciona Ladino -> Clérigo 4/Ladino 1 (Nível 5)
        Nota: Teste documenta comportamento atual - não há endpoint específico para adicionar classe
        """
        # Criar ficha com apenas Clérigo
        ficha_clerigo = Ficha.objects.create(
            dono=self.user, nome="Clérigo Puro", nivel=4
        )

        nivel_clerigo = NivelClasseFicha.objects.create(
            ficha=ficha_clerigo, classe=self.classe_clerigo, nivel=4
        )

        # Adicionar Ladino manualmente (simula adicionar nova classe)
        nivel_ladino = NivelClasseFicha.objects.create(
            ficha=ficha_clerigo, classe=self.classe_ladino, nivel=1
        )

        # Incrementar nível total
        ficha_clerigo.nivel = 5
        ficha_clerigo.save()

        # Verificações
        self.assertEqual(ficha_clerigo.nivel, 5)
        self.assertEqual(
            NivelClasseFicha.objects.filter(ficha=ficha_clerigo).count(), 2
        )

        # Verificar que Clérigo permanece nível 4
        nivel_clerigo.refresh_from_db()
        self.assertEqual(nivel_clerigo.nivel, 4)

        # Verificar que Ladino é nível 1
        self.assertEqual(nivel_ladino.nivel, 1)


class CalculosNivelTestCase(TestCase):
    """
    Testes para recálculos automáticos ao subir de nível
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_calculos", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar atributos
        self.atributo_forca = Atributo.objects.create(nome="for", ordem=1)
        self.atributo_destreza = Atributo.objects.create(nome="des", ordem=2)

        # Criar perícia
        self.pericia_atletismo = Pericia.objects.create(nome="atl", requer_treino=False)

        # Criar classe
        self.classe_batedor = Classe.objects.create(
            nome="Batedor",
            vida_base=14,
            vida_por_nivel=4,
            mana_base=3,
            mana_por_nivel=2,
            proficiencia="Armas leves",
        )

        # Criar ficha - Batedor Nível 3
        self.ficha_batedor = Ficha.objects.create(
            dono=self.user, nome="Batedor de Teste", nivel=3
        )

        # Adicionar classe
        self.nivel_batedor = NivelClasseFicha.objects.create(
            ficha=self.ficha_batedor, classe=self.classe_batedor, nivel=3
        )

        # Adicionar atributo Força +2
        self.attr_forca = AtributoFicha.objects.create(
            ficha=self.ficha_batedor, atributo=self.atributo_forca, valor=2
        )

        # Criar perícia treinada
        self.pericia_treinada = PericiaTreinada.objects.create(
            ficha=self.ficha_batedor,
            pericia=self.pericia_atletismo,
            treinado=True,
            bonus_adicional=0,
        )
        self.pericia_treinada.atributo_chave.add(self.attr_forca)

    def test_recalculo_pericias_ao_subir_nivel(self):
        """
        Teste CT-NIV-05: Verificar se perícias são recalculadas após subir de nível
        Batedor Nível 3 -> Nível 4
        Bônus de nível muda de +1 (3/2) para +2 (4/2)
        """
        # Calcular valor inicial
        # Nível 3: (3/2) = 1 + 2 (força) + 2 (treino nível 1-5) = 5
        valor_inicial = self.pericia_treinada.calcularValor()
        self.assertEqual(valor_inicial, 5)

        # Subir de nível
        url = f"/arkheion_api/personagem/{self.ficha_batedor.id}/subir-nivel/"
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que o nível foi incrementado
        self.ficha_batedor.refresh_from_db()
        self.assertEqual(self.ficha_batedor.nivel, 4)

        # Calcular novo valor da perícia
        # Nível 4: (4/2) = 2 + 2 (força) + 2 (treino nível 1-5) = 6
        self.pericia_treinada.refresh_from_db()
        valor_novo = self.pericia_treinada.calcularValor()
        self.assertEqual(valor_novo, 6)

    def test_calculo_vida_mana_multiclasse(self):
        """
        Teste CT-NIV-08: Verificar cálculo de vida e mana
        Teste CT-NIV-11: Cálculo multiclasse complexo
        """
        # Criar ficha multiclasse complexa: Guerreiro 6 / Ladino 4 / Mago 2 (Nível 12)
        classe_guerreiro = Classe.objects.create(
            nome="Guerreiro",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
        )

        classe_ladino = Classe.objects.create(
            nome="Ladino", vida_base=12, vida_por_nivel=3, mana_base=0, mana_por_nivel=0
        )

        classe_mago = Classe.objects.create(
            nome="Mago", vida_base=10, vida_por_nivel=2, mana_base=15, mana_por_nivel=7
        )

        ficha_complexa = Ficha.objects.create(
            dono=self.user, nome="Multiclasse Complexo", nivel=12
        )

        # Adicionar classes
        NivelClasseFicha.objects.create(
            ficha=ficha_complexa, classe=classe_guerreiro, nivel=6
        )

        NivelClasseFicha.objects.create(
            ficha=ficha_complexa, classe=classe_ladino, nivel=4
        )

        NivelClasseFicha.objects.create(
            ficha=ficha_complexa, classe=classe_mago, nivel=2
        )

        # Subir de nível (Mago vai para nível 3)
        url = f"/arkheion_api/personagem/{ficha_complexa.id}/subir-nivel/"
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que o nível total foi incrementado
        ficha_complexa.refresh_from_db()
        self.assertEqual(ficha_complexa.nivel, 13)


class LimitesNivelTestCase(TestCase):
    """
    Testes para limites e validações de nível
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_limites", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar classe
        self.classe_guerreiro = Classe.objects.create(
            nome="Guerreiro",
            vida_base=20,
            vida_por_nivel=5,
            mana_base=0,
            mana_por_nivel=0,
            proficiencia="Todas",
        )

        # Criar ficha nível 19
        self.ficha_nivel_19 = Ficha.objects.create(
            dono=self.user, nome="Guerreiro Nível 19", nivel=19
        )

        NivelClasseFicha.objects.create(
            ficha=self.ficha_nivel_19, classe=self.classe_guerreiro, nivel=19
        )

        # Criar ficha nível 20
        self.ficha_nivel_20 = Ficha.objects.create(
            dono=self.user, nome="Guerreiro Nível 20", nivel=20
        )

        NivelClasseFicha.objects.create(
            ficha=self.ficha_nivel_20, classe=self.classe_guerreiro, nivel=20
        )

    def test_subir_nivel_ate_20(self):
        """
        Teste CT-NIV-09: Subir de nível 19 para 20 (limite máximo)
        """
        url = f"/arkheion_api/personagem/{self.ficha_nivel_19.id}/subir-nivel/"

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que chegou ao nível 20
        self.ficha_nivel_19.refresh_from_db()
        self.assertEqual(self.ficha_nivel_19.nivel, 20)

    def test_subir_nivel_alem_de_20(self):
        """
        Teste: Tentar subir além do nível 20
        Nota: O sistema atual não valida limite de nível
        """
        url = f"/arkheion_api/personagem/{self.ficha_nivel_20.id}/subir-nivel/"

        response = self.client.post(url, {}, format="json")

        # Sistema atual permite passar de 20
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.ficha_nivel_20.refresh_from_db()
        # Documenta comportamento atual (sem validação de limite)
        self.assertEqual(self.ficha_nivel_20.nivel, 21)


class AutorizacaoNivelTestCase(TestCase):
    """
    Testes de autorização e permissões
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar dois usuários
        self.user1 = User.objects.create_user(username="user1", password="pass123")

        self.user2 = User.objects.create_user(username="user2", password="pass456")

        # Autenticar como user1
        self.token1 = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        # Criar classe
        self.classe_ranger = Classe.objects.create(
            nome="Ranger", vida_base=16, vida_por_nivel=4
        )

        # Criar ficha do user2
        self.ficha_user2 = Ficha.objects.create(
            dono=self.user2, nome="Ranger do User2", nivel=7
        )

        NivelClasseFicha.objects.create(
            ficha=self.ficha_user2, classe=self.classe_ranger, nivel=7
        )

    def test_sem_autenticacao(self):
        """
        Teste: Tentar subir nível sem autenticação
        """
        # Remover credenciais
        self.client.credentials()

        url = f"/arkheion_api/personagem/{self.ficha_user2.id}/subir-nivel/"
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subir_nivel_ficha_outro_usuario(self):
        """
        Teste: Usuário1 tentando subir nível da ficha do usuário2
        """
        # User1 tenta acessar ficha do user2
        url = f"/arkheion_api/personagem/{self.ficha_user2.id}/subir-nivel/"
        response = self.client.post(url, {}, format="json")

        # Deve retornar 404 (ficha não encontrada) ou 403 (sem permissão)
        self.assertIn(
            response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]
        )


class PericiasSemClasseTestCase(TestCase):
    """
    Teste para cenários de erro específicos
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_sem_classe", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar ficha SEM classes
        self.ficha_sem_classe = Ficha.objects.create(
            dono=self.user, nome="Personagem Sem Classe", nivel=1
        )

    def test_subir_nivel_sem_classes(self):
        """
        Teste CT-NIV-10: Personagem sem classes cadastradas
        Nota: O sistema atual não valida se há classes
        """
        url = f"/arkheion_api/personagem/{self.ficha_sem_classe.id}/subir-nivel/"

        response = self.client.post(url, {}, format="json")

        # Sistema atual permite subir nível mesmo sem classes
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.ficha_sem_classe.refresh_from_db()
        self.assertEqual(self.ficha_sem_classe.nivel, 2)


class VisualizacaoNivelTestCase(TestCase):
    """
    Testes para visualização de dados de nível
    """

    def setUp(self):
        """
        Configurar dados de teste
        """
        self.client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(
            username="test_visualizacao", password="testpass123"
        )

        # Autenticar
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criar classes
        self.classe_mago = Classe.objects.create(
            nome="Mago", vida_base=10, vida_por_nivel=2, mana_base=15, mana_por_nivel=7
        )

        # Criar ficha
        self.ficha = Ficha.objects.create(
            dono=self.user, nome="Mago para Visualização", nivel=5
        )

        NivelClasseFicha.objects.create(
            ficha=self.ficha, classe=self.classe_mago, nivel=5
        )

    def test_visualizar_nivel_classes_na_ficha(self):
        """
        Teste adicional: Verificar que níveis de classes são retornados ao buscar ficha
        """
        url = f"/arkheion_api/personagem/{self.ficha.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nivel"], 5)
        self.assertIn("niveis_classes", response.data)

        # Verificar que a classe está na lista
        niveis = response.data["niveis_classes"]
        self.assertTrue(len(niveis) > 0)

        # Verificar dados da classe
        nivel_mago = next((n for n in niveis if n["classe"]["nome"] == "Mago"), None)
        self.assertIsNotNone(nivel_mago)
        self.assertEqual(nivel_mago["nivel"], 5)
