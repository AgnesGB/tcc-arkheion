#!/bin/bash

# Script para atualizar automaticamente o IP/DNS público do master AWS
# Detecta automaticamente da instância EC2 ou permite configuração manual
#
# Uso:
#   ./update-ip.sh                                    # Modo interativo/automático
#   ./update-ip.sh 3.81.166.171                      # Apenas IP
#   ./update-ip.sh ec2-3-81-166-171.compute-1.amazonaws.com  # Apenas DNS (recomendado)
#   ./update-ip.sh --use-dns                         # Força uso do DNS auto-detectado

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Atualizador de IP/DNS do Master AWS ===${NC}\n"

# Se recebeu argumento, usa direto
if [ $# -ge 1 ] && [ "$1" != "--use-dns" ]; then
    BACKEND_HOST="$1"
    echo -e "${GREEN}✓ Usando host fornecido:${NC} $BACKEND_HOST"
    
    # Tenta detectar mais informações se possível
    if curl -s -m 2 http://169.254.169.254/latest/meta-data/public-ipv4 > /dev/null 2>&1; then
        PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
        PUBLIC_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
        echo -e "${YELLOW}Informações EC2 detectadas:${NC}"
        echo "  IP:  $PUBLIC_IP"
        echo "  DNS: $PUBLIC_DNS"
    fi
    
# Verifica se está rodando em uma instância EC2
elif curl -s -m 2 http://169.254.169.254/latest/meta-data/public-ipv4 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Detectada instância EC2${NC}"
    
    # Obtém informações automaticamente
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
    PUBLIC_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
    PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
    
    echo -e "${YELLOW}Informações detectadas:${NC}"
    echo "  IP Público:  $PUBLIC_IP"
    echo "  DNS Público: $PUBLIC_DNS"
    echo "  IP Privado:  $PRIVATE_IP"
    echo ""
    
    # Pergunta se quer usar DNS ou IP
    read -p "Deseja usar DNS público (mais estável) ou IP? [D/i]: " choice
    case "$choice" in
        i|I)
            BACKEND_HOST="$PUBLIC_IP"
            ;;
        *)
            BACKEND_HOST="$PUBLIC_DNS"
            ;;
    esac
else
    echo -e "${YELLOW}⚠ Não está rodando em instância EC2${NC}"
    echo "Digite as informações manualmente:"
    echo ""
    
    # Valores padrão do último conhecimento
    DEFAULT_IP="3.81.166.171"
    DEFAULT_DNS="ec2-3-81-166-171.compute-1.amazonaws.com"
    
    read -p "IP Público [$DEFAULT_IP]: " PUBLIC_IP
    PUBLIC_IP=${PUBLIC_IP:-$DEFAULT_IP}
    
    read -p "DNS Público [$DEFAULT_DNS]: " PUBLIC_DNS
    PUBLIC_DNS=${PUBLIC_DNS:-$DEFAULT_DNS}
    
    # Pergunta se quer usar DNS ou IP
    echo ""
    read -p "Deseja usar DNS público (recomendado) ou IP? [D/i]: " choice
    case "$choice" in
        i|I)
            BACKEND_HOST="$PUBLIC_IP"
            ;;
        *)
            BACKEND_HOST="$PUBLIC_DNS"
            ;;
    esac
fi

BACKEND_PORT="30080"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}/arkheion_api"

echo ""
echo -e "${GREEN}URL do backend configurada:${NC} $BACKEND_URL"
echo ""

# Atualiza .env.production do frontend
echo -e "${YELLOW}Atualizando frontend/.env.production...${NC}"
cat > frontend/.env.production <<EOF
VITE_BACKEND_URL=$BACKEND_URL
EOF
echo -e "${GREEN}✓ frontend/.env.production atualizado${NC}"

# Atualiza Dockerfile.frontend.prod
echo -e "${YELLOW}Atualizando Dockerfile.frontend.prod...${NC}"
if [ -f "Dockerfile.frontend.prod" ]; then
    # Backup
    cp Dockerfile.frontend.prod Dockerfile.frontend.prod.bak
    
    # Substitui a linha do ARG VITE_BACKEND_URL
    sed -i "s|^ARG VITE_BACKEND_URL=.*|ARG VITE_BACKEND_URL=$BACKEND_URL|" Dockerfile.frontend.prod
    
    echo -e "${GREEN}✓ Dockerfile.frontend.prod atualizado${NC}"
    echo -e "${YELLOW}  (backup salvo em Dockerfile.frontend.prod.bak)${NC}"
fi

# Cria/atualiza .env.aws com as informações
echo -e "${YELLOW}Criando .env.aws...${NC}"
cat > .env.aws <<EOF
# Configurações do Master AWS
# Gerado automaticamente em $(date)

AWS_MASTER_PUBLIC_IP=$PUBLIC_IP
AWS_MASTER_PUBLIC_DNS=$PUBLIC_DNS
AWS_MASTER_BACKEND_URL=$BACKEND_URL
AWS_MASTER_BACKEND_PORT=$BACKEND_PORT
EOF
echo -e "${GREEN}✓ .env.aws criado${NC}"

echo ""
echo -e "${GREEN}=== Atualização concluída com sucesso! ===${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "  1. Faça rebuild da imagem do frontend:"
echo -e "     ${GREEN}docker build -f Dockerfile.frontend.prod -t arkheion-frontend:latest .${NC}"
echo ""
echo "  2. Ou se estiver usando deploy-app.sh no master, execute:"
echo -e "     ${GREEN}./aws/deploy-app.sh${NC}"
echo ""
echo -e "${YELLOW}Dica:${NC} Configure este script para rodar automaticamente no master"
echo "     adicionando ao final do setup-master.sh ou deploy-app.sh"
