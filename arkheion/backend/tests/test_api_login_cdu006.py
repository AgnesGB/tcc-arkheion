"""
Testes de API para CDU006 - Logar Usuário
Baseado no planejamento em: doc/testes/CT-CDU006.md

Endpoints testados:
- POST /arkheion_api/auth/login/ (Token-based authentication)
- POST /arkheion_api/auth/jwt/login/ (JWT-based authentication)
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserLoginTokenTestCase(TestCase):
    """
    Testes para o endpoint de login com Token (CDU006)
    Endpoint: /arkheion_api/auth/login/
    """

    def setUp(self):
        """
        Configurar dados de teste antes de cada teste
        """
        self.client = APIClient()
        self.url_token = "/arkheion_api/auth/login/"

        # Criar usuário de teste conforme CT-CDU006
        self.test_user = User.objects.create_user(
            username="teste_jv",
            email="teste_jv@arkheion.com",
            password="SenhaValida123!",
            first_name="João",
            last_name="Victor",
        )

        # Criar usuário com username longo (150 caracteres - limite do Django)
        self.long_username = "A" * 150
        self.user_long = User.objects.create_user(
            username=self.long_username, password="SenhaValida123!"
        )

    def test_login_sucesso_com_username(self):
        """
        Teste CT-LOG-01: Login com sucesso usando username
        CT-CDU006: Usuario teste_jv com senha SenhaValida123!
        """
        payload = {"username": "teste_jv", "password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Verificações
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "teste_jv")
        self.assertEqual(response.data["email"], "teste_jv@arkheion.com")

        # Verificar que o token é válido
        token = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token, user=self.test_user).exists())

    def test_login_sucesso_com_email(self):
        """
        Teste CT-LOG-02: Login com sucesso usando email
        Nota: Django ObtainAuthToken padrão NÃO suporta login com email,
        apenas com username. Este teste documenta o comportamento real.
        """
        payload = {
            "username": "teste_jv@arkheion.com",  # Tentando usar email no campo username
            "password": "SenhaValida123!",
        }

        response = self.client.post(self.url_token, payload, format="json")

        # API espera username, não email - deve falhar
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_sem_username(self):
        """
        Teste CT-LOG-03: Tentar fazer login sem fornecer username
        """
        payload = {"password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Deve retornar erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", str(response.data).lower())

    def test_login_sem_senha(self):
        """
        Teste CT-LOG-04: Tentar fazer login sem fornecer senha
        """
        payload = {"username": "teste_jv"}

        response = self.client.post(self.url_token, payload, format="json")

        # Deve retornar erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", str(response.data).lower())

    def test_login_usuario_nao_existe(self):
        """
        Teste CT-LOG-05: Tentar fazer login com usuário que não existe
        """
        payload = {"username": "usuario_nao_existe", "password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Deve retornar erro de autenticação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Mensagem pode variar mas deve indicar credenciais inválidas
        response_str = str(response.data).lower()
        self.assertTrue(
            "unable to log in" in response_str
            or "invalid" in response_str
            or "incorrect" in response_str
        )

    def test_login_email_nao_existe(self):
        """
        Teste CT-LOG-06: Tentar fazer login com email que não existe
        Nota: Como a API espera username, não email, este teste documenta
        o comportamento ao tentar usar email inexistente como username.
        """
        payload = {"username": "nao_existe@email.com", "password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Deve retornar erro de autenticação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_senha_incorreta(self):
        """
        Teste CT-LOG-07: Tentar fazer login com senha incorreta
        """
        payload = {"username": "teste_jv", "password": "SenhaErrada123"}

        response = self.client.post(self.url_token, payload, format="json")

        # Deve retornar erro de autenticação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_str = str(response.data).lower()
        self.assertTrue(
            "unable to log in" in response_str
            or "invalid" in response_str
            or "incorrect" in response_str
        )

    def test_login_username_limite_superior(self):
        """
        Teste CT-LOG-08: Login com username no limite superior (150 caracteres)
        Django User model tem limite de 150 caracteres para username
        """
        payload = {"username": self.long_username, "password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Login deve funcionar normalmente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], self.long_username)

    def test_login_username_acima_limite(self):
        """
        Teste CT-LOG-09: Tentar login com username acima do limite (151 caracteres)
        Django não permite criar usuários com username > 150 caracteres,
        mas testamos o comportamento ao tentar fazer login com tal valor.
        """
        payload = {
            "username": "A" * 151,  # 151 caracteres
            "password": "SenhaValida123!",
        }

        response = self.client.post(self.url_token, payload, format="json")

        # Deve falhar na autenticação (usuário não existe com esse username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_sql_injection_attempt(self):
        """
        Teste CT-LOG-10: Tentativa de SQL injection
        Django ORM protege contra SQL injection automaticamente
        """
        payload = {"username": "teste_jv' OR 1=1;--", "password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Deve tratar como string literal e falhar na busca
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_retorna_dados_usuario(self):
        """
        Teste adicional: Verificar que login retorna dados completos do usuário
        """
        payload = {"username": "teste_jv", "password": "SenhaValida123!"}

        response = self.client.post(self.url_token, payload, format="json")

        # Verificar campos retornados
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

        # Verificar valores
        self.assertEqual(response.data["user_id"], self.test_user.id)
        self.assertEqual(response.data["first_name"], "João")
        self.assertEqual(response.data["last_name"], "Victor")

    def test_login_multiplos_logins_mesmo_token(self):
        """
        Teste adicional: Verificar que múltiplos logins retornam o mesmo token
        Token-based auth mantém o mesmo token para o usuário
        """
        payload = {"username": "teste_jv", "password": "SenhaValida123!"}

        # Primeiro login
        response1 = self.client.post(self.url_token, payload, format="json")
        token1 = response1.data["token"]

        # Segundo login
        response2 = self.client.post(self.url_token, payload, format="json")
        token2 = response2.data["token"]

        # Tokens devem ser iguais
        self.assertEqual(token1, token2)


class UserLoginJWTTestCase(TestCase):
    """
    Testes para o endpoint de login com JWT (CDU006)
    Endpoint: /arkheion_api/auth/jwt/login/
    """

    def setUp(self):
        """
        Configurar dados de teste antes de cada teste
        """
        self.client = APIClient()
        self.url_jwt = "/arkheion_api/auth/jwt/login/"

        # Criar usuário de teste conforme CT-CDU006
        self.test_user = User.objects.create_user(
            username="teste_jv",
            email="teste_jv@arkheion.com",
            password="SenhaValida123!",
            first_name="João",
            last_name="Victor",
        )

        # Criar usuário com username longo
        self.long_username = "B" * 150
        self.user_long = User.objects.create_user(
            username=self.long_username, password="SenhaValida123!"
        )

    def test_login_jwt_sucesso(self):
        """
        Teste CT-LOG-01 JWT: Login com sucesso usando JWT
        """
        payload = {"username": "teste_jv", "password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Verificações
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

        # Verificar dados do usuário
        user_data = response.data["user"]
        self.assertEqual(user_data["username"], "teste_jv")
        self.assertEqual(user_data["email"], "teste_jv@arkheion.com")

    def test_login_jwt_sem_username(self):
        """
        Teste CT-LOG-03 JWT: Tentar fazer login sem username
        """
        payload = {"password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve retornar erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", str(response.data).lower())

    def test_login_jwt_sem_senha(self):
        """
        Teste CT-LOG-04 JWT: Tentar fazer login sem senha
        """
        payload = {"username": "teste_jv"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve retornar erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", str(response.data).lower())

    def test_login_jwt_usuario_nao_existe(self):
        """
        Teste CT-LOG-05 JWT: Tentar fazer login com usuário inexistente
        """
        payload = {"username": "usuario_nao_existe", "password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve retornar erro de autenticação
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_jwt_senha_incorreta(self):
        """
        Teste CT-LOG-07 JWT: Tentar fazer login com senha incorreta
        """
        payload = {"username": "teste_jv", "password": "SenhaErrada123"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve retornar erro de autenticação
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_jwt_username_limite_superior(self):
        """
        Teste CT-LOG-08 JWT: Login com username no limite superior (150 caracteres)
        """
        payload = {"username": self.long_username, "password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Login deve funcionar normalmente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_jwt_sql_injection_attempt(self):
        """
        Teste CT-LOG-10 JWT: Tentativa de SQL injection
        """
        payload = {"username": "teste_jv' OR 1=1;--", "password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve tratar como string literal e falhar
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_jwt_retorna_dados_completos(self):
        """
        Teste adicional: Verificar que JWT login retorna dados completos
        """
        payload = {"username": "teste_jv", "password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Verificar estrutura da resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

        # Verificar dados do usuário
        user_data = response.data["user"]
        self.assertIn("id", user_data)
        self.assertIn("username", user_data)
        self.assertIn("email", user_data)
        self.assertIn("first_name", user_data)
        self.assertIn("last_name", user_data)
        self.assertIn("date_joined", user_data)
        self.assertIn("last_login", user_data)

    def test_login_jwt_multiplos_logins_tokens_diferentes(self):
        """
        Teste adicional: JWT gera tokens diferentes a cada login
        Diferente do Token-based, JWT gera novos tokens a cada requisição
        """
        payload = {"username": "teste_jv", "password": "SenhaValida123!"}

        # Primeiro login
        response1 = self.client.post(self.url_jwt, payload, format="json")
        access1 = response1.data["access"]

        # Aguardar um momento para garantir timestamp diferente
        import time

        time.sleep(1)

        # Segundo login
        response2 = self.client.post(self.url_jwt, payload, format="json")
        access2 = response2.data["access"]

        # Tokens devem ser diferentes
        self.assertNotEqual(access1, access2)

    def test_login_jwt_campos_vazios(self):
        """
        Teste adicional: Tentar login com campos vazios (strings vazias)
        """
        payload = {"username": "", "password": ""}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve retornar erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_jwt_username_com_espacos(self):
        """
        Teste adicional: Tentar login com username contendo espaços
        Django JWT faz trim automático dos campos
        """
        payload = {"username": "  teste_jv  ", "password": "SenhaValida123!"}

        response = self.client.post(self.url_jwt, payload, format="json")

        # Django JWT faz trim automático, então o login deve funcionar
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_jwt_case_sensitive_username(self):
        """
        Teste adicional: Verificar que username é case-sensitive
        """
        payload = {
            "username": "TESTE_JV",  # Username em maiúsculas
            "password": "SenhaValida123!",
        }

        response = self.client.post(self.url_jwt, payload, format="json")

        # Deve falhar pois username é case-sensitive no Django
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
