# Aliases e Funções Úteis para o Projeto Arkheion
# 
# Para usar, adicione ao seu ~/.bashrc ou ~/.bash_aliases:
# source /caminho/para/Arkheion/.bash_aliases
#
# Ou copie as funções que desejar para seu .bashrc

# =============================================================================
# ATUALIZAÇÃO DE IP AWS
# =============================================================================

# Função para atualizar IP do AWS rapidamente
update_arkheion_ip() {
    local SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    if [ $# -eq 0 ]; then
        echo "Uso: update_arkheion_ip <DNS-ou-IP>"
        echo ""
        echo "Exemplos:"
        echo "  update_arkheion_ip ec2-3-81-166-171.compute-1.amazonaws.com"
        echo "  update_arkheion_ip 3.81.166.171"
        return 1
    fi
    
    "$SCRIPT_DIR/update-ip.sh" "$1"
}

# Alias curto
alias uip='update_arkheion_ip'

# =============================================================================
# INFORMAÇÕES DO CLUSTER
# =============================================================================

# Ver informações rápidas do cluster
alias k3s-info='kubectl cluster-info && echo "" && kubectl get nodes'

# Ver status dos deployments do Arkheion
alias arkheion-status='kubectl get deployments,services,pods -o wide | grep -E "(NAME|arkheion|backend|frontend|postgres)"'

# Logs do backend
alias arkheion-logs-backend='kubectl logs -f deployment/backend'

# Logs do frontend
alias arkheion-logs-frontend='kubectl logs -f deployment/frontend'

# =============================================================================
# DESENVOLVIMENTO LOCAL
# =============================================================================

# Subir ambiente de desenvolvimento
alias arkheion-dev-up='docker-compose -f docker-compose.dev.yml up -d'

# Parar ambiente de desenvolvimento
alias arkheion-dev-down='docker-compose -f docker-compose.dev.yml down'

# Ver logs do dev
alias arkheion-dev-logs='docker-compose -f docker-compose.dev.yml logs -f'

# =============================================================================
# BUILD E DEPLOY
# =============================================================================

# Build completo (frontend + backend)
arkheion-build-all() {
    local DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    echo "🔨 Building frontend..."
    docker build -f "$DIR/Dockerfile.frontend.prod" -t arkheion-frontend:latest "$DIR"
    
    echo ""
    echo "🔨 Building backend..."
    docker build -f "$DIR/Dockerfile.prod" -t arkheion-backend:latest "$DIR/arkheion"
    
    echo ""
    echo "✅ Build completo!"
}

# Deploy rápido no K3S
arkheion-deploy() {
    local DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    if [ ! -f "$DIR/aws/deploy-app.sh" ]; then
        echo "❌ Script de deploy não encontrado!"
        return 1
    fi
    
    cd "$DIR/aws"
    ./deploy-app.sh
}

# =============================================================================
# UTILIDADES
# =============================================================================

# Mostrar IP/DNS atual configurado
arkheion-show-config() {
    local DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    echo "📝 Configuração atual:"
    echo ""
    
    if [ -f "$DIR/.env.aws" ]; then
        echo "Arquivo .env.aws:"
        cat "$DIR/.env.aws" | grep -v "^#" | grep -v "^$"
        echo ""
    fi
    
    if [ -f "$DIR/frontend/.env.production" ]; then
        echo "Frontend (.env.production):"
        cat "$DIR/frontend/.env.production"
        echo ""
    fi
}

# Ver informações da instância EC2 (se rodando nela)
arkheion-ec2-info() {
    if curl -s -m 2 http://169.254.169.254/latest/meta-data/public-ipv4 > /dev/null 2>&1; then
        echo "📡 Informações da Instância EC2:"
        echo ""
        echo "IP Público:  $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
        echo "DNS Público: $(curl -s http://169.254.169.254/latest/meta-data/public-hostname)"
        echo "IP Privado:  $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)"
        echo "Zona:        $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)"
        echo "Tipo:        $(curl -s http://169.254.169.254/latest/meta-data/instance-type)"
    else
        echo "❌ Não está rodando em uma instância EC2"
        return 1
    fi
}

# =============================================================================
# HELP
# =============================================================================

arkheion-help() {
    cat << 'EOF'
🎮 Comandos Arkheion Disponíveis:

📍 Atualização de IP:
  update_arkheion_ip <dns-ou-ip>  Atualiza IP/DNS do master AWS
  uip <dns-ou-ip>                  Atalho para update_arkheion_ip
  arkheion-show-config             Mostra configuração atual
  arkheion-ec2-info                Info da instância EC2 (se aplicável)

🔍 Cluster K3S:
  k3s-info                         Informações do cluster
  arkheion-status                  Status dos deployments
  arkheion-logs-backend            Logs do backend
  arkheion-logs-frontend           Logs do frontend

💻 Desenvolvimento Local:
  arkheion-dev-up                  Sobe ambiente dev
  arkheion-dev-down                Para ambiente dev
  arkheion-dev-logs                Logs do ambiente dev

🚀 Build e Deploy:
  arkheion-build-all               Build frontend + backend
  arkheion-deploy                  Deploy no K3S

📚 Este Help:
  arkheion-help                    Mostra este help

Exemplos de uso:
  $ uip ec2-3-81-166-171.compute-1.amazonaws.com
  $ arkheion-build-all && arkheion-deploy
  $ arkheion-status
EOF
}

# Mostra mensagem de carregamento
echo "✅ Aliases do Arkheion carregados! Digite 'arkheion-help' para ver comandos disponíveis."
