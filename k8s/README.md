# Manifestos Kubernetes (k3s) - Arkheion

## 📋 Estrutura dos Manifestos

```
k8s/
├── postgres-pvc.yaml              # PersistentVolumeClaim do banco
├── postgres-configmap.yaml        # ConfigMap do PostgreSQL
├── postgres-secret.yaml           # Secret do PostgreSQL
├── postgres-deployment.yaml       # Deployment + Service do PostgreSQL
├── backend-configmap.yaml         # ConfigMap do Backend Django
├── backend-secret.yaml            # Secret do Backend
├── backend-deployment.yaml        # Deployment + Service do Backend (5 réplicas)
├── frontend-configmap.yaml        # ConfigMap do Frontend Vue.js
├── frontend-deployment.yaml       # Deployment + Service do Frontend (5 réplicas)
├── frontend-ingress.yaml          # Ingress com Traefik (acesso externo)
└── setup-k3s.sh                   # Script de instalação e deploy automatizado
```

## 🎯 Decisões de Arquitetura

### 1. PostgreSQL (Stateful)
**Decisão:** 1 réplica com PersistentVolumeClaim

**Por quê:**
- Banco de dados é stateful, não deve ter múltiplas réplicas sem replicação configurada
- PVC garante persistência dos dados mesmo se o pod morrer
- Service tipo ClusterIP (interno) - apenas backend acessa

**Recursos:**
- Memory: 256Mi request / 512Mi limit
- CPU: 250m request / 500m limit

### 2. Backend Django (Stateless)
**Decisão:** 5 réplicas com load balancing automático

**Por quê:**
- Aplicação stateless, pode escalar horizontalmente
- 5 réplicas conforme requisito do trabalho
- Service tipo ClusterIP - acesso interno do cluster
- ConfigMap/Secret separam configuração de código

**Recursos por pod:**
- Memory: 256Mi request / 512Mi limit
- CPU: 250m request / 500m limit

**Healthchecks:**
- Liveness: verifica se o pod está vivo (path: `/admin/`)
- Readiness: verifica se o pod está pronto para receber tráfego

### 3. Frontend Vue.js (Stateless)
**Decisão:** 5 réplicas com NodePort

**Por quê:**
- Aplicação stateless, escala horizontalmente
- 5 réplicas conforme requisito
- Service tipo NodePort para acesso externo (porta 30173)
- Em produção na AWS, usaremos LoadBalancer ou Ingress

**Recursos por pod:**
- Memory: 256Mi request / 512Mi limit
- CPU: 250m request / 500m limit

## 🔐 Secrets e ConfigMaps

### Por que separar?
- **Secrets:** Dados sensíveis (senhas, tokens, chaves)
- **ConfigMaps:** Configurações não-sensíveis (URLs, flags, nomes)

### Vantagem no Kubernetes:
- Mudanças em ConfigMap/Secret não exigem rebuild da imagem
- Mesma imagem roda em dev/staging/prod com configs diferentes
- Secrets são criptografados em repouso (com configuração adequada)

## 🚀 Setup com k3s

### Pré-requisitos
- Docker instalado (para build das imagens)
- k3s instalado (ou use o script automatizado)

### Opção 1: Script Automatizado (Recomendado)

```bash
# Dar permissão de execução
chmod +x k8s/setup-k3s.sh

# Executar (instala k3s se necessário e faz deploy)
./k8s/setup-k3s.sh
```

### Opção 2: Manual

#### 1. Instalar k3s

```bash
# Instalar k3s (leve e rápido)
curl -sfL https://get.k3s.io | sh -

# Dar permissão ao kubectl config
sudo chmod 644 /etc/rancher/k3s/k3s.yaml

# Configurar KUBECONFIG (adicionar ao ~/.bashrc para persistir)
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

#### 2. Build das imagens Docker

```bash
# Backend
docker build -f Dockerfile -t arkheion_backend:latest .

# Frontend
docker build -f Dockerfile.frontend -t arkheion_frontend:latest .
```

#### 3. Importar imagens para k3s

```bash
# k3s usa containerd, então precisamos importar as imagens
sudo k3s ctr images import <(docker save arkheion_backend:latest)
sudo k3s ctr images import <(docker save arkheion_frontend:latest)

# Ou salvar e importar
docker save arkheion_backend:latest -o /tmp/backend.tar
docker save arkheion_frontend:latest -o /tmp/frontend.tar
sudo k3s ctr images import /tmp/backend.tar
sudo k3s ctr images import /tmp/frontend.tar
```

#### 4. Aplicar manifestos Kubernetes

```bash
cd k8s

# 1. Secrets e ConfigMaps
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-configmap.yaml
kubectl apply -f backend-secret.yaml
kubectl apply -f backend-configmap.yaml
kubectl apply -f frontend-configmap.yaml

# 2. PVC
kubectl apply -f postgres-pvc.yaml

# 3. Banco de dados
kubectl apply -f postgres-deployment.yaml

# 4. Aguardar postgres estar ready (pode demorar ~30s)
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s

# 5. Backend
kubectl apply -f backend-deployment.yaml

# 6. Aguardar backend estar ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=180s

# 7. Frontend
kubectl apply -f frontend-deployment.yaml

# 8. Ingress (opcional, mas recomendado)
kubectl apply -f frontend-ingress.yaml
```

## 📊 Verificação e Acesso

```bash
# Ver todos os recursos
kubectl get all

# Ver pods e seu status
kubectl get pods

# Ver services e seus endpoints
kubectl get svc

# Ver ingress
kubectl get ingress

# Ver logs de um pod
kubectl logs <pod-name>

# Ver logs em tempo real
kubectl logs -f <pod-name>

# Acessar shell de um pod
kubectl exec -it <pod-name> -- /bin/sh
```

### Acessar a Aplicação

**Opção 1: Via Ingress (Recomendado)**
```bash
# Descobrir IP do nó k3s
kubectl get nodes -o wide

# Acessar pelo navegador
# http://<NODE_IP>  (Traefik escuta na porta 80)
# ou
# http://arkheion.local (se configurou /etc/hosts)
```

**Opção 2: Via NodePort**
```bash
# Frontend: http://<NODE_IP>:30173
# Ex: http://192.168.1.100:30173
```

**Opção 3: Port Forward (Desenvolvimento)**
```bash
# Frontend
kubectl port-forward svc/frontend 8080:5173

# Backend
kubectl port-forward svc/backend 8000:8000

# Acessar: http://localhost:8080
```

### Configurar /etc/hosts (Opcional)

```bash
# Adicionar ao /etc/hosts para usar arkheion.local
echo "127.0.0.1 arkheion.local" | sudo tee -a /etc/hosts

# Agora pode acessar: http://arkheion.local
```

## 🔄 Diferenças: Docker Compose vs k3s

| Aspecto | Docker Compose | k3s (Kubernetes) |
|---------|---------------|------------------|
| **Escala** | Manual (`docker-compose up --scale`) | Declarativa (`replicas: 5`) |
| **Persistência** | Volumes nomeados | PersistentVolumeClaim + local-path |
| **Config** | `.env` ou `environment` | ConfigMap + Secret |
| **Networking** | Bridge network | Service DNS + Ingress |
| **Load Balancing** | Não tem (precisa nginx) | Nativo via Service + Traefik |
| **Health Checks** | healthcheck | livenessProbe/readinessProbe |
| **Ingress** | Precisa configurar proxy | Traefik embutido |
| **Tamanho** | Docker Engine (~500MB) | k3s (~100MB) |
| **Uso** | Desenvolvimento local | Dev + Produção |

## 🎓 Para o Professor

**Justificativa técnica das escolhas:**

1. **k3s vs kind:** k3s é mais leve (100MB vs 500MB), certificado CNCF, usado em produção, e vem com Traefik embutido
2. **5 réplicas:** Atende requisito + demonstra alta disponibilidade e load balancing
3. **Service ClusterIP (backend/db):** Segurança - não expõe ao mundo externo
4. **Ingress com Traefik:** Substitui NodePort, mais profissional e próximo de produção
5. **PVC com local-path:** StorageClass padrão do k3s, persistência garantida
6. **ConfigMap/Secret:** Segue best practice 12-factor app
7. **Resource Limits:** Previne um pod consumir todo o cluster
8. **Probes:** Kubernetes sabe quando reiniciar ou remover pod do balanceamento
9. **imagePullPolicy: IfNotPresent:** Funciona com registry local do k3s

**Vantagens do k3s:**

- ✅ Kubernetes certificado e completo
- ✅ Metade do tamanho do k8s tradicional
- ✅ Ingress Controller (Traefik) já incluído
- ✅ StorageClass (local-path) pré-configurado
- ✅ Ideal para edge, IoT, e ambientes com recursos limitados
- ✅ Mesma API do Kubernetes, fácil migrar para EKS/AKS/GKE

**Próximos passos (AWS EKS):**

- Trocar storageClassName para `gp3` (EBS da AWS)
- Usar AWS Load Balancer Controller para Ingress
- Configurar certificado SSL com cert-manager
- Adicionar Horizontal Pod Autoscaler (HPA)
- Implementar NetworkPolicies para segurança
- Usar AWS Secrets Manager para secrets

## 🧹 Limpeza

```bash
# Deletar todos os recursos
kubectl delete -f k8s/

# Ou deletar serviços específicos
kubectl delete deployment,service,ingress,configmap,secret,pvc -l app=arkheion

# Desinstalar k3s completamente
/usr/local/bin/k3s-uninstall.sh
```

## 🐛 Troubleshooting

### Pods não iniciam

```bash
# Ver eventos do pod
kubectl describe pod <pod-name>

# Ver logs detalhados
kubectl logs <pod-name> --previous

# Ver se a imagem foi importada corretamente
sudo k3s crictl images
```

### Ingress não funciona

```bash
# Verificar se Traefik está rodando
kubectl get pods -n kube-system | grep traefik

# Ver logs do Traefik
kubectl logs -n kube-system -l app.kubernetes.io/name=traefik
```

### Banco de dados não conecta

```bash
# Verificar se o PVC foi criado
kubectl get pvc

# Verificar se o volume foi montado
kubectl describe pod -l app=postgres
```

## 📚 Recursos Adicionais

- [Documentação k3s](https://docs.k3s.io/)
- [Traefik Ingress](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
