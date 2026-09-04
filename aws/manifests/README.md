# README - Manifestos AWS

## 📁 Estrutura

Todos os manifestos K8S necessários para deploy na AWS estão nesta pasta.

## 🚀 Ordem de Deploy

### 1. PostgreSQL (Banco de Dados)
```bash
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-configmap.yaml
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-deployment.yaml  # Inclui deployment + service
```

**Aguardar PostgreSQL ficar pronto:**
```bash
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
```

### 2. Backend (Django API)
```bash
kubectl apply -f backend-configmap.yaml
kubectl apply -f backend-secret.yaml
kubectl apply -f backend-deployment.yaml
```

**Aguardar Backend ficar pronto:**
```bash
kubectl wait --for=condition=ready pod -l app=backend --timeout=180s
```

### 3. Frontend (Vue.js)
```bash
kubectl apply -f frontend-configmap.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
```

**Aguardar Frontend ficar pronto:**
```bash
kubectl wait --for=condition=ready pod -l app=frontend --timeout=120s
```

### 4. Opcional: Ingress
```bash
kubectl apply -f frontend-ingress.yaml
```

## 🔍 Verificação

```bash
# Ver todos os pods
kubectl get pods -A

# Ver services
kubectl get svc -A

# Ver deployments
kubectl get deployments

# Verificar réplicas
kubectl get pods -l app=backend    # Deve ter 5
kubectl get pods -l app=frontend   # Deve ter 5
```

## 🌐 Acessar Aplicação

### Via NodePort (Padrão)
```
http://<PUBLIC_IP_MASTER>:30173
http://<PUBLIC_IP_WORKER1>:30173
http://<PUBLIC_IP_WORKER2>:30173
```

### Via LoadBalancer (Se habilitado)
```bash
kubectl get svc frontend-lb
# Usar EXTERNAL-IP
```

## ⚙️ Diferenças para Ambiente Local

### 1. ImagePullPolicy
- **Local:** `IfNotPresent` (usa imagem local)
- **AWS:** `Always` (sempre baixa do Docker Hub)

### 2. Service Frontend
- **Local:** Pode usar ClusterIP + Ingress
- **AWS:** NodePort (acesso direto) ou LoadBalancer (custo extra)

### 3. PostgreSQL Storage
- **Local:** K3S local-path provisioner
- **AWS:** K3S local-path provisioner (poderia usar EBS para produção)

### 4. Imagens
- **Local:** `arkheion_backend:latest` (local)
- **AWS:** `walber147/arkheion_backend:latest` (Docker Hub)

## 🔧 Ajustes Necessários

### Backend ConfigMap
Verificar se `ALLOWED_HOSTS` inclui:
- IP público das instâncias
- Nome de domínio (se tiver)
- LoadBalancer DNS (se usar)

### Frontend ConfigMap
Ajustar `VITE_BACKEND_URL`:
- NodePort: `http://<PUBLIC_IP>:30173`
- LoadBalancer: `http://<LB_DNS>`

## 💰 Custos

### Com NodePort (Atual)
- **Custo:** $0 extra
- **Acesso:** Via IP público + porta
- **Limitação:** Porta alta (30000-32767)

### Com LoadBalancer
- **Custo:** ~$18/mês (Network Load Balancer)
- **Acesso:** Via DNS do LoadBalancer
- **Vantagem:** Porta 80/443 padrão

## 🛡️ Segurança

### Secrets em Produção Real
Para produção real, considere:
- AWS Secrets Manager
- External Secrets Operator
- Sealed Secrets

### Network Policies
Adicionar policies para isolar tráfego:
```yaml
# Exemplo: Frontend só acessa Backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

## 📊 Monitoramento

### Logs
```bash
# Ver logs de um pod
kubectl logs <POD_NAME>

# Seguir logs em tempo real
kubectl logs -f <POD_NAME>

# Logs de todos os pods de um deployment
kubectl logs -l app=backend --tail=50
```

### Métricas
```bash
# Uso de recursos
kubectl top nodes
kubectl top pods
```

### Eventos
```bash
# Ver eventos do cluster
kubectl get events --sort-by=.metadata.creationTimestamp

# Eventos de um pod específico
kubectl describe pod <POD_NAME>
```

## 🔄 Atualização de Imagens

Quando atualizar a imagem no Docker Hub:

```bash
# Forçar pull da nova imagem
kubectl rollout restart deployment/backend
kubectl rollout restart deployment/frontend

# Verificar rollout
kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend
```

## 🐛 Troubleshooting

### Pods em CrashLoopBackOff
```bash
kubectl logs <POD_NAME>
kubectl describe pod <POD_NAME>
```

### Service não acessível
```bash
# Verificar endpoints
kubectl get endpoints

# Testar de dentro do cluster
kubectl run test --image=busybox -it --rm -- sh
wget -O- http://backend:8000/api/
```

### Imagem não baixa
```bash
# Verificar eventos do pod
kubectl describe pod <POD_NAME>

# Verificar se imagem existe
docker pull walber147/arkheion_backend:latest
```

---

**Boa sorte no deploy! 🚀**
