"""
Testes unitários para serializers de autenticação
"""

from django.test import TestCase
from django.contrib.auth.models import User
from backend.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
)


class UserSerializerTest(TestCase):
    """Testes para UserSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_serializer_com_instancia(self):
        """Testa serialização de usuário"""
        serializer = UserSerializer(instance=self.user)
        data = serializer.data

        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["last_name"], "User")

    def test_serializer_campos_read_only(self):
        """Testa campos read_only"""
        UserSerializer(instance=self.user)

        self.assertIn("id", UserSerializer.Meta.read_only_fields)
        self.assertIn("date_joined", UserSerializer.Meta.read_only_fields)
        self.assertIn("last_login", UserSerializer.Meta.read_only_fields)

    def test_serializer_campos_presentes(self):
        """Testa que todos os campos esperados estão presentes"""
        serializer = UserSerializer(instance=self.user)
        expected_fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        ]

        for field in expected_fields:
            self.assertIn(field, serializer.data)


class UserRegistrationSerializerTest(TestCase):
    """Testes para UserRegistrationSerializer"""

    def test_serializer_criar_usuario_valido(self):
        """Testa criação de usuário válido"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
            "first_name": "New",
            "last_name": "User",
        }
        serializer = UserRegistrationSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("securepass123"))

    def test_serializer_senhas_nao_coincidem(self):
        """Testa validação quando senhas não coincidem"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "pass123",
            "password_confirm": "pass456",
        }
        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_serializer_senha_muito_curta(self):
        """Testa validação de senha muito curta"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "123",
            "password_confirm": "123",
        }
        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_email_duplicado(self):
        """Testa validação de email duplicado"""
        # Criar usuário existente
        User.objects.create_user(
            username="existing", email="existing@example.com", password="pass123"
        )

        # Tentar criar com mesmo email
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "pass123",
            "password_confirm": "pass123",
        }
        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_serializer_username_duplicado(self):
        """Testa validação de username duplicado"""
        # Criar usuário existente
        User.objects.create_user(
            username="existing", email="existing@example.com", password="pass123"
        )

        # Tentar criar com mesmo username
        data = {
            "username": "existing",
            "email": "newemail@example.com",
            "password": "pass123",
            "password_confirm": "pass123",
        }
        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        # Pode estar em 'non_field_errors' ou 'username'
        self.assertTrue(
            "non_field_errors" in serializer.errors or "username" in serializer.errors
        )

    def test_serializer_email_obrigatorio(self):
        """Testa que email é obrigatório"""
        data = {
            "username": "newuser",
            "password": "pass123",
            "password_confirm": "pass123",
        }
        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_serializer_campos_write_only(self):
        """Testa que senha não aparece na serialização"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Serializar o usuário criado
        read_serializer = UserRegistrationSerializer(instance=user)

        # Senha não deve aparecer
        self.assertNotIn("password", read_serializer.data)
        self.assertNotIn("password_confirm", read_serializer.data)


class CustomTokenObtainPairSerializerTest(TestCase):
    """Testes para CustomTokenObtainPairSerializer"""

    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_serializer_dados_usuario_incluidos(self):
        """Testa que dados do usuário são incluídos no token"""
        data = {"username": "testuser", "password": "testpass123"}
        serializer = CustomTokenObtainPairSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data

        # Verificar que dados do usuário estão incluídos
        self.assertIn("user", validated_data)
        self.assertEqual(validated_data["user"]["username"], "testuser")
        self.assertEqual(validated_data["user"]["email"], "test@example.com")

    def test_serializer_tokens_gerados(self):
        """Testa que tokens são gerados"""
        data = {"username": "testuser", "password": "testpass123"}
        serializer = CustomTokenObtainPairSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        # Verificar que tokens estão presentes
        self.assertIn("access", validated_data)
        self.assertIn("refresh", validated_data)

    def test_serializer_credenciais_invalidas(self):
        """Testa validação com credenciais inválidas"""
        from rest_framework.exceptions import AuthenticationFailed

        data = {"username": "testuser", "password": "wrongpass"}
        serializer = CustomTokenObtainPairSerializer(data=data)

        # O serializer lança exceção para credenciais inválidas
        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)
