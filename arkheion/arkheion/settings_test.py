"""
Configurações para testes do Arkheion
Utiliza SQLite para facilitar a execução dos testes sem necessidade do PostgreSQL
"""

from datetime import timedelta
from .settings import *  # noqa: F401, F403
from .settings import SIMPLE_JWT

# Usar SQLite para testes
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # Usar banco de dados em memória para testes mais rápidos
    }
}

# Desabilitar logging durante os testes
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}

# Usar um SECRET_KEY fixo para testes
SECRET_KEY = "test-secret-key-for-testing-purposes-only"

# Desabilitar verificações de senha para testes mais rápidos
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Desabilitar debug durante testes
DEBUG = False

# Simplificar configurações de JWT para testes
SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=30)
SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] = timedelta(days=1)
