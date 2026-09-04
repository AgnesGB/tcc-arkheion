# ✅ Checklist Completo - Apresentação Arkheion K3S

## 📋 Pré-Apresentação

### Infraestrutura AWS
- [ ] 3 instâncias EC2 criadas e rodando
  - [ ] k3s-master (t3.small)
  - [ ] k3s-worker-1 (t3.micro)
  - [ ] k3s-worker-2 (t3.micro)
- [ ] Security group `k3s-cluster` configurado
- [ ] Key pair salva em local seguro
- [ ] IPs públicos anotados

### Cluster K3S
- [ ] Master instalado e rodando
- [ ] Workers conectados ao master
- [ ] `kubectl get nodes` mostra 3 nós Ready

### Aplicação
- [ ] PostgreSQL rodando (1 réplica)
- [ ] Backend rodando (5 réplicas)
- [ ] Frontend rodando (5 réplicas)
- [ ] Aplicação acessível via browser
- [ ] Consegue criar conta e fazer login
- [ ] Consegue criar personagem
- [ ] Dados persistem após refresh

---

## 🎤 Roteiro de Apresentação

### 1. Introdução (2 minutos)
**O que mostrar:**
- Nome do projeto: Arkheion
- Objetivo: Sistema de fichas de RPG
- Stack: Django + Vue.js + PostgreSQL
- Deploy: K3S na AWS

**Falar:**
> "Vou apresentar o Arkheion, um sistema de gerenciamento de fichas de RPG desenvolvido em Django e Vue.js, deployado em um cluster Kubernetes usando K3S na AWS com 3 nós e alta disponibilidade."

### 2. Arquitetura (3 minutos)
**Diagrama no quadro/slide:**
```
┌─────────────────────────────────────┐
│         AWS Cloud                    │
│                                      │
│  EC2 Master (K3S Server)            │
│       - Control Plane                │
│       - Scheduling                   │
│                                      │
│  EC2 Worker 1 (K3S Agent)           │
│       - Backend Pods (réplicas)      │
│       - Frontend Pods (réplicas)     │
│                                      │
│  EC2 Worker 2 (K3S Agent)           │
│       - Backend Pods (réplicas)      │
│       - Frontend Pods (réplicas)     │
│       - PostgreSQL Pod               │
└─────────────────────────────────────┘
```

**Decisões para explicar:**
- ✅ **Por que K3S:** Leve, certificado, produção-ready
- ✅ **Por que 3 nós:** Master dedicado + 2 workers (HA)
- ✅ **Por que 5 réplicas:** Alta disponibilidade e load balancing
- ✅ **Services:** Abstração de rede, descoberta automática
- ✅ **NodePort:** Acesso externo sem custo de LoadBalancer

### 3. Demonstração Técnica (5 minutos)

#### 3.1 Mostrar Cluster
```bash
# SSH no master
ssh -i k3s-key.pem ubuntu@<MASTER_IP>

# Mostrar nós (DEVE TER 3)
kubectl get nodes

# Explicar: Master (control-plane) + 2 Workers
```

**O que falar:**
> "Temos 3 nós no cluster: 1 master rodando o control plane do K3S e 2 workers onde os pods da aplicação estão distribuídos."

#### 3.2 Mostrar Deployments
```bash
# Ver deployments
kubectl get deployments

# Mostrar detalhes
kubectl get deployment backend
kubectl get deployment frontend
```

**O que falar:**
> "Criamos dois deployments principais: backend com Django e frontend com Vue.js, cada um configurado para 5 réplicas."

#### 3.3 Mostrar Réplicas do Backend
```bash
# Ver pods do backend (DEVE TER 5)
kubectl get pods -l app=backend

# Mostrar detalhes de um pod
kubectl describe pod <BACKEND_POD_NAME>
```

**O que falar:**
> "Aqui estão as 5 réplicas do backend rodando. Cada pod tem 256Mi de RAM e 250m de CPU configurados como request, com limites de 512Mi e 500m."

#### 3.4 Mostrar Réplicas do Frontend
```bash
# Ver pods do frontend (DEVE TER 5)
kubectl get pods -l app=frontend

# Mostrar distribuição nos nós
kubectl get pods -l app=frontend -o wide
```

**O que falar:**
> "As 5 réplicas do frontend estão distribuídas entre os workers. O scheduler do Kubernetes distribui automaticamente para balancear a carga."

#### 3.5 Mostrar Services
```bash
# Ver todos os services
kubectl get svc

# Explicar cada um:
# - postgres: ClusterIP (interno)
# - backend: ClusterIP (interno)
# - frontend: NodePort (externo)
```

**O que falar:**
> "Usamos Services para abstração de rede. PostgreSQL e backend são ClusterIP (acesso interno apenas). O frontend é NodePort para acesso externo na porta 30173."

#### 3.6 Mostrar Conectividade
```bash
# Testar conectividade interna
kubectl exec -it <FRONTEND_POD> -- /bin/sh
wget -O- http://backend:8000/api/

# OU mostrar logs do backend sendo acessado
kubectl logs -l app=backend --tail=20
```

**O que falar:**
> "O frontend se comunica com o backend através do Service 'backend' na porta 8000. O DNS interno do Kubernetes resolve automaticamente."

### 4. Demonstração Funcional (3 minutos)

#### 4.1 Acessar Aplicação
**No browser:**
```
http://<MASTER_PUBLIC_IP>:30173
```

#### 4.2 Fluxo de Teste
1. **Tela inicial:** Mostrar interface
2. **Criar conta:** Cadastrar novo usuário
3. **Login:** Autenticar
4. **Dashboard:** Mostrar painel
5. **Criar personagem:** Criar nova ficha
6. **Editar personagem:** Modificar atributos
7. **Verificar persistência:** Refresh da página

**O que falar:**
> "A aplicação está totalmente funcional. Vou criar um personagem para demonstrar a persistência de dados no PostgreSQL e a comunicação entre frontend, backend e banco."

### 5. Manifests YAML (2 minutos)

**Mostrar arquivos principais:**

```bash
# Backend Deployment
cat ~/manifests/backend-deployment.yaml | grep -A 10 "replicas\|image\|resources"

# Frontend Deployment
cat ~/manifests/frontend-deployment.yaml | grep -A 10 "replicas\|image\|resources"

# Services
cat ~/manifests/frontend-service.yaml
```

**Explicar:**
- **replicas: 5** - Quantidade de pods
- **image: walber147/arkheion_backend:latest** - Imagem no Docker Hub
- **imagePullPolicy: Always** - Sempre baixa versão mais recente
- **resources** - Limits e requests de CPU/RAM
- **Service NodePort** - Expõe na porta 30173

### 6. Alta Disponibilidade (2 minutos)

#### Demonstrar HA
```bash
# Deletar um pod do backend
kubectl delete pod <BACKEND_POD_NAME>

# Mostrar que K8S cria automaticamente
watch kubectl get pods -l app=backend

# Aplicação continua funcionando!
```

**O que falar:**
> "Vou deletar um pod do backend para demonstrar a auto-recuperação. O Kubernetes detecta e cria um novo pod automaticamente, mantendo sempre 5 réplicas. A aplicação não sofre downtime."

### 7. Escalabilidade (1 minuto)

```bash
# Escalar para 10 réplicas
kubectl scale deployment/backend --replicas=10

# Ver pods sendo criados
kubectl get pods -l app=backend -w

# Voltar para 5
kubectl scale deployment/backend --replicas=5
```

**O que falar:**
> "Podemos escalar horizontalmente com um comando simples. Aqui estou aumentando de 5 para 10 réplicas. Em produção, poderíamos usar HPA (Horizontal Pod Autoscaler) para escalar automaticamente baseado em métricas."

### 8. Perguntas Comuns

#### "Por que não usou LoadBalancer?"
> "LoadBalancer na AWS custa ~$18/mês extra. Para ambiente acadêmico, NodePort é suficiente e gratuito. Em produção, usaríamos LoadBalancer ou Ingress com certificado SSL."

#### "Os dados persistem se reiniciar a instância?"
> "Sim, usamos PersistentVolumeClaim para o PostgreSQL. Os dados ficam no volume EBS da AWS. Em produção, poderíamos usar RDS."

#### "Por que K3S e não K8S completo?"
> "K3S é certificado pela CNCF, usa menos recursos (ideal para VMs pequenas), tem setup mais simples, mas mantém compatibilidade total com K8S. Perfeito para edge computing e ambientes com recursos limitados."

#### "Como faz deploy de uma nova versão?"
> "Build da nova imagem, push para Docker Hub, e executar kubectl rollout restart. O K8S faz rolling update sem downtime."

#### "E se um worker morrer?"
> "Os pods são redistribuídos para os nós disponíveis automaticamente. Com PodDisruptionBudget, garantimos disponibilidade mínima durante manutenções."

---

## 📊 Comandos para Copiar/Colar Durante Apresentação

```bash
# Nós do cluster
kubectl get nodes

# Deployments
kubectl get deployments

# Pods do backend (5 réplicas)
kubectl get pods -l app=backend

# Pods do frontend (5 réplicas)
kubectl get pods -l app=frontend

# Distribuição nos nós
kubectl get pods -o wide

# Services
kubectl get svc

# Detalhes de um deployment
kubectl describe deployment backend

# Logs
kubectl logs -l app=backend --tail=20

# Deletar pod (demonstrar HA)
kubectl delete pod <POD_NAME>

# Escalar
kubectl scale deployment/backend --replicas=10

# Watch (acompanhar mudanças)
watch kubectl get pods -l app=backend
```

---

## 🎯 Pontos Importantes para Enfatizar

### Requisitos Atendidos
✅ Cluster Kubernetes real (K3S)  
✅ Mínimo 2 nós (temos 3)  
✅ Distribuição de produção (K3S)  
✅ VMs na nuvem (AWS EC2)  
✅ Deploy com manifests YAML  
✅ 5 réplicas de backend e frontend  
✅ Services para conectividade  
✅ Sistema 100% funcional  

### Diferenciais
🌟 Master dedicado (boas práticas)  
🌟 Alta disponibilidade (5 réplicas)  
🌟 Auto-recuperação (K8S self-healing)  
🌟 Escalabilidade horizontal  
🌟 Persistent storage (PostgreSQL)  
🌟 Imagens no Docker Hub (CI/CD ready)  
🌟 Resource limits (QoS garantido)  
🌟 Health checks (liveness/readiness probes)  

---

## 🐛 Troubleshooting Pré-Apresentação

### Se algo não estiver funcionando:

**Pods em CrashLoopBackOff:**
```bash
kubectl logs <POD_NAME>
kubectl describe pod <POD_NAME>
kubectl rollout restart deployment/<NAME>
```

**Frontend não acessa backend:**
```bash
# Verificar DNS interno
kubectl exec -it <FRONTEND_POD> -- nslookup backend

# Verificar service endpoints
kubectl get endpoints backend
```

**Aplicação não acessível:**
```bash
# Verificar NodePort
kubectl get svc frontend

# Verificar security group permite porta 30173

# Testar diretamente no master
curl http://localhost:30173
```

**Worker desconectado:**
```bash
# No worker, verificar serviço
sudo systemctl status k3s-agent

# Restart se necessário
sudo systemctl restart k3s-agent

# Ver logs
sudo journalctl -u k3s-agent -f
```

---

## ⏰ Timeline Sugerida

- **00:00-02:00** - Introdução e contexto
- **02:00-05:00** - Arquitetura e decisões
- **05:00-10:00** - Demonstração técnica (kubectl)
- **10:00-13:00** - Demonstração funcional (browser)
- **13:00-15:00** - Manifests e configurações
- **15:00-17:00** - Alta disponibilidade
- **17:00-18:00** - Escalabilidade
- **18:00-20:00** - Perguntas

---

## 📸 Screenshots Recomendados

Tire prints antes para ter backup:
1. `kubectl get nodes`
2. `kubectl get deployments`
3. `kubectl get pods -o wide`
4. `kubectl get svc`
5. Aplicação no browser funcionando
6. Dashboard AWS com 3 instâncias EC2

---

**Boa apresentação! 🚀🎉**
