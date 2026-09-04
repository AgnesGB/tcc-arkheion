# Imagem base do Python
FROM python:3.12-slim

# Variáveis de ambiente básicas para o Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# (Opcional) Instalar dependências de sistema.
# Por enquanto só build-essential para compilar libs se precisar.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas o requirements.txt do backend
COPY arkheion/requirements.txt /app/requirements.txt

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do backend (pasta arkheion inteira)
COPY arkheion /app

# Expor a porta em que o Django vai rodar
EXPOSE 8000

# Comando padrão:
# - roda as migrações
# - sobe o servidor de desenvolvimento acessível externamente
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]