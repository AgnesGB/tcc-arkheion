#!/bin/bash
#
# Script de instalação e deploy do Arkheion no k3s
# Uso: ./setup-k3s.sh
#

set -e  # Parar em caso de erro

echo "========================================="
echo "  Arkheion - Setup k3s Automatizado"
echo "========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se está rodando como root (necessário para instalar k3s)
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        print_warn "Não execute este script como root. Ele solicitará sudo quando necessário."
        exit 1
    fi
}

# Verificar se k3s está instalado
check_k3s() {
    if command -v k3s &> /dev/null; then
        print_info "k3s já está instalado ($(k3s --version | head -1))"
        return 0
    else
        print_warn "k3s não encontrado"
        return 1
    fi
}

# Instalar k3s
install_k3s() {
    print_info "Instalando k3s..."
    curl -sfL https://get.k3s.io | sh -
    
    print_info "Aguardando k3s inicializar..."
    sleep 10
    
    # Configurar permissões
    sudo chmod 644 /etc/rancher/k3s/k3s.yaml
    
    print_info "k3s instalado com sucesso!"
}

# Configurar KUBECONFIG
setup_kubeconfig() {
    export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
    
    # Adicionar ao bashrc se ainda não estiver lá
    if ! grep -q "KUBECONFIG=/etc/rancher/k3s/k3s.yaml" ~/.bashrc; then
        echo "export KUBECONFIG=/etc/rancher/k3s/k3s.yaml" >> ~/.bashrc
        print_info "KUBECONFIG adicionado ao ~/.bashrc"
    fi
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado. Por favor, instale Docker primeiro."
        exit 1
    fi
    print_info "Docker encontrado ($(docker --version))"
}

# Build das imagens Docker
build_images() {
    print_info "Construindo imagens Docker..."
    
    cd /home/walber/Projetos/Arkheion
    
    # Backend
    print_info "Building backend..."
    docker build -f Dockerfile -t arkheion_backend:latest .
    
    # Frontend
    print_info "Building frontend..."
    docker build -f Dockerfile.frontend -t arkheion_frontend:latest .
    
    print_info "Imagens construídas com sucesso!"
}

# Importar imagens para k3s
import_images() {
    print_info "Importando imagens para k3s..."
    
    # Salvar imagens
    docker save arkheion_backend:latest -o /tmp/arkheion_backend.tar
    docker save arkheion_frontend:latest -o /tmp/arkheion_frontend.tar
    
    # Importar para k3s
    sudo k3s ctr images import /tmp/arkheion_backend.tar
    sudo k3s ctr images import /tmp/arkheion_frontend.tar
    
    # Limpar arquivos temporários
    rm -f /tmp/arkheion_backend.tar /tmp/arkheion_frontend.tar
    
    print_info "Imagens importadas para k3s!"
}

# Aplicar manifestos Kubernetes
apply_manifests() {
    print_info "Aplicando manifestos Kubernetes..."
    
    cd /home/walber/Projetos/Arkheion/k8s
    
    # 1. Secrets e ConfigMaps
    print_info "Aplicando Secrets e ConfigMaps..."
    kubectl apply -f postgres-secret.yaml
    kubectl apply -f postgres-configmap.yaml
    kubectl apply -f backend-secret.yaml
    kubectl apply -f backend-configmap.yaml
    kubectl apply -f frontend-configmap.yaml
    
    # 2. PVC
    print_info "Criando PersistentVolumeClaim..."
    kubectl apply -f postgres-pvc.yaml
    
    # 3. PostgreSQL
    print_info "Deployando PostgreSQL..."
    kubectl apply -f postgres-deployment.yaml
    
    print_info "Aguardando PostgreSQL ficar pronto (pode demorar ~30s)..."
    kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s || print_warn "Postgres demorou mais que o esperado"
    
    # 4. Backend
    print_info "Deployando Backend (5 réplicas)..."
    kubectl apply -f backend-deployment.yaml
    
    print_info "Aguardando Backend ficar pronto (pode demorar ~60s)..."
    kubectl wait --for=condition=ready pod -l app=backend --timeout=180s || print_warn "Backend demorou mais que o esperado"
    
    # 5. Frontend
    print_info "Deployando Frontend (5 réplicas)..."
    kubectl apply -f frontend-deployment.yaml
    
    # 6. Ingress
    print_info "Configurando Ingress..."
    kubectl apply -f frontend-ingress.yaml
    
    print_info "Todos os manifestos aplicados!"
}

# Mostrar status
show_status() {
    echo ""
    echo "========================================="
    echo "  Status do Cluster"
    echo "========================================="
    echo ""
    
    kubectl get nodes
    echo ""
    kubectl get pods
    echo ""
    kubectl get svc
    echo ""
    kubectl get ingress
}

# Mostrar instruções de acesso
show_access_info() {
    echo ""
    echo "========================================="
    echo "  Como Acessar a Aplicação"
    echo "========================================="
    echo ""
    
    NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
    
    echo -e "${GREEN}Opção 1: Via Ingress (Recomendado)${NC}"
    echo "  http://$NODE_IP"
    echo ""
    
    echo -e "${GREEN}Opção 2: Via NodePort${NC}"
    echo "  http://$NODE_IP:30173"
    echo ""
    
    echo -e "${GREEN}Opção 3: Configurar hostname local${NC}"
    echo "  sudo echo '$NODE_IP arkheion.local' >> /etc/hosts"
    echo "  http://arkheion.local"
    echo ""
    
    echo -e "${YELLOW}Comandos úteis:${NC}"
    echo "  kubectl get pods              # Ver status dos pods"
    echo "  kubectl logs <pod-name>       # Ver logs de um pod"
    echo "  kubectl get all               # Ver todos os recursos"
    echo ""
}

# Main
main() {
    check_sudo
    
    # 1. Verificar e instalar k3s
    if ! check_k3s; then
        print_info "Instalando k3s..."
        install_k3s
    fi
    
    # 2. Configurar KUBECONFIG
    setup_kubeconfig
    
    # 3. Verificar Docker
    check_docker
    
    # 4. Build das imagens
    read -p "Deseja fazer build das imagens Docker? (s/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        build_images
        import_images
    else
        print_warn "Pulando build. Certifique-se de que as imagens já existem no k3s."
    fi
    
    # 5. Aplicar manifestos
    apply_manifests
    
    # 6. Aguardar um pouco para estabilizar
    print_info "Aguardando cluster estabilizar..."
    sleep 10
    
    # 7. Mostrar status
    show_status
    
    # 8. Mostrar instruções de acesso
    show_access_info
    
    echo ""
    print_info "Setup concluído com sucesso! 🚀"
}

# Executar
main "$@"
