# 🚀 Deploy Arkheion na AWS com K3S

## 📋 Requisitos da Atividade

✅ Cluster Kubernetes (K3S) em produção  
✅ Mínimo 2 nós (usaremos 3: 1 master + 2 workers)  
✅ Máquinas Virtuais na AWS (EC2)  
✅ Deploy com 5 réplicas  
✅ Frontend e Backend conectados via Services  

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│          AWS Cloud (Região)             │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Security Group (k3s-cluster)   │  │
│  │   - 22 (SSH)                     │  │
│  │   - 6443 (K3S API)               │  │
│  │   - 80/443 (HTTP/HTTPS)          │  │
│  │   - 8472 (Flannel VXLAN)         │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  EC2 Master (t3.small)            │ │
│  │  - K3S Server                     │ │
│  │  - 2 vCPU, 2GB RAM                │ │
│  │  - IP Público + Privado           │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  EC2 Worker 1 (t3.micro)          │ │
│  │  - K3S Agent                      │ │
│  │  - 2 vCPU, 1GB RAM                │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  EC2 Worker 2 (t3.micro)          │ │
│  │  - K3S Agent                      │ │
│  │  - 2 vCPU, 1GB RAM                │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**Custo estimado:** ~$30/mês (cabe em $50!)

---

## 🎯 Passo a Passo Completo

### Fase 1: Preparação AWS

#### 1.1 Criar Security Group

```bash
# Via Console AWS ou AWS CLI
aws ec2 create-security-group \
  --group-name k3s-cluster \
  --description "Security group for K3S cluster"

# Adicionar regras
aws ec2 authorize-security-group-ingress \
  --group-name k3s-cluster \
  --protocol tcp --port 22 --cidr 0.0.0.0/0       # SSH
  
aws ec2 authorize-security-group-ingress \
  --group-name k3s-cluster \
  --protocol tcp --port 6443 --cidr 0.0.0.0/0     # K3S API
  
aws ec2 authorize-security-group-ingress \
  --group-name k3s-cluster \
  --protocol tcp --port 80 --cidr 0.0.0.0/0       # HTTP
  
aws ec2 authorize-security-group-ingress \
  --group-name k3s-cluster \
  --protocol tcp --port 443 --cidr 0.0.0.0/0      # HTTPS
  
aws ec2 authorize-security-group-ingress \
  --group-name k3s-cluster \
  --protocol udp --port 8472 --cidr 10.0.0.0/8    # Flannel VXLAN
  
# Liberar tráfego entre nós do cluster
aws ec2 authorize-security-group-ingress \
  --group-name k3s-cluster \
  --source-group k3s-cluster \
  --protocol all
```

**OU pelo Console AWS:**

1. EC2 → Security Groups → Create security group
2. Nome: `k3s-cluster`
3. Adicionar Inbound Rules:
   - SSH (22) - My IP (ou 0.0.0.0/0)
   - Custom TCP (6443) - 0.0.0.0/0
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom UDP (8472) - 10.0.0.0/8
   - All traffic - Source: k3s-cluster (próprio security group)

#### 1.2 Criar Par de Chaves SSH

```bash
# Via AWS CLI
aws ec2 create-key-pair --key-name k3s-key --query 'KeyMaterial' --output text > k3s-key.pem
chmod 400 k3s-key.pem
```

**OU pelo Console:**
1. EC2 → Key Pairs → Create key pair
2. Nome: `k3s-key`
3. Tipo: RSA
4. Formato: .pem
5. Salvar o arquivo em local seguro

#### 1.3 Criar Instâncias EC2

**Master Node:**
- AMI: Ubuntu Server 22.04 LTS
- Tipo: t3.small (2 vCPU, 2GB RAM)
- Storage: 20GB GP3
- Security Group: k3s-cluster
- Key pair: k3s-key
- **Tag Name:** k3s-master

**Worker Node 1:**
- AMI: Ubuntu Server 22.04 LTS
- Tipo: t3.micro (2 vCPU, 1GB RAM)
- Storage: 15GB GP3
- Security Group: k3s-cluster
- Key pair: k3s-key
- **Tag Name:** k3s-worker-1

**Worker Node 2:**
- AMI: Ubuntu Server 22.04 LTS
- Tipo: t3.micro (2 vCPU, 1GB RAM)
- Storage: 15GB GP3
- Security Group: k3s-cluster
- Key pair: k3s-key
- **Tag Name:** k3s-worker-2

---

### Fase 2: Instalação do Cluster K3S

#### 2.1 Anotar IPs das Instâncias

Após criar as instâncias, anote:
```
MASTER_PUBLIC_IP=<IP_PÚBLICO_MASTER>
MASTER_PRIVATE_IP=<IP_PRIVADO_MASTER>
WORKER1_PUBLIC_IP=<IP_PÚBLICO_WORKER1>
WORKER2_PUBLIC_IP=<IP_PÚBLICO_WORKER2>
```

#### 2.2 Setup do Master Node

**SSH no Master:**
```bash
ssh -i k3s-key.pem ubuntu@$MASTER_PUBLIC_IP
```

**Baixar e executar script de setup:**
```bash
# Fazer upload do setup-master.sh ou colar o conteúdo
nano setup-master.sh
# Cole o conteúdo do arquivo aws/setup-master.sh

chmod +x setup-master.sh
./setup-master.sh
```

**Após instalação, pegar o token:**
```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

**Salvar o token:** `K10<LONG_TOKEN_STRING>::server:<RANDOM>`

#### 2.3 Setup dos Worker Nodes

**SSH no Worker 1:**
```bash
ssh -i k3s-key.pem ubuntu@$WORKER1_PUBLIC_IP
```

**Baixar e executar script:**
```bash
nano setup-worker.sh
# Cole o conteúdo e substitua:
# - K3S_URL pela URL do master
# - K3S_TOKEN pelo token obtido

chmod +x setup-worker.sh
./setup-worker.sh
```

**Repetir para Worker 2**

#### 2.4 Verificar Cluster

**No Master:**
```bash
sudo kubectl get nodes
```

**Saída esperada:**
```
NAME           STATUS   ROLES                  AGE   VERSION
k3s-master     Ready    control-plane,master   5m    v1.28.x+k3s1
k3s-worker-1   Ready    <none>                 2m    v1.28.x+k3s1
k3s-worker-2   Ready    <none>                 2m    v1.28.x+k3s1
```

---

### Fase 3: Deploy da Aplicação

#### 3.1 Copiar Manifestos para o Master

**No seu computador local:**
```bash
# Copiar pasta de manifestos
scp -i k3s-key.pem -r aws/manifests ubuntu@$MASTER_PUBLIC_IP:~/
```

**OU criar manualmente no master:**
```bash
ssh -i k3s-key.pem ubuntu@$MASTER_PUBLIC_IP
mkdir -p ~/manifests
cd ~/manifests

# Criar cada arquivo (veja seção Manifestos abaixo)
```

#### 3.2 Deploy do PostgreSQL

```bash
sudo kubectl apply -f manifests/postgres-pvc.yaml
sudo kubectl apply -f manifests/postgres-configmap.yaml
sudo kubectl apply -f manifests/postgres-secret.yaml
sudo kubectl apply -f manifests/postgres-deployment.yaml  # Inclui deployment + service
```

**Verificar:**
```bash
sudo kubectl get pods -l app=postgres
sudo kubectl get svc postgres
```

#### 3.3 Deploy do Backend

```bash
sudo kubectl apply -f manifests/backend-configmap.yaml
sudo kubectl apply -f manifests/backend-secret.yaml
sudo kubectl apply -f manifests/backend-deployment.yaml
```

**Verificar:**
```bash
sudo kubectl get pods -l app=backend
sudo kubectl get svc backend
```

#### 3.4 Deploy do Frontend

```bash
sudo kubectl apply -f manifests/frontend-configmap.yaml
sudo kubectl apply -f manifests/frontend-deployment.yaml
sudo kubectl apply -f manifests/frontend-service.yaml
```

**Verificar:**
```bash
sudo kubectl get pods -l app=frontend
sudo kubectl get svc frontend
```

#### 3.5 Acessar a Aplicação

**NodePort (temporário):**
```
http://<MASTER_PUBLIC_IP>:30173
```

**LoadBalancer (após configurar - opcional):**
```bash
sudo kubectl get svc frontend
# Usar EXTERNAL-IP quando disponível
```

---

### Fase 4: Verificação e Testes

#### 4.1 Verificar Pods

```bash
# Ver todos os pods
sudo kubectl get pods -A

# Ver detalhes de um pod específico
sudo kubectl describe pod <POD_NAME>

# Ver logs
sudo kubectl logs <POD_NAME>
```

#### 4.2 Verificar Services

```bash
sudo kubectl get svc -A
```

#### 4.3 Verificar Réplicas

```bash
# Backend (deve ter 5)
sudo kubectl get deployment backend
sudo kubectl get pods -l app=backend

# Frontend (deve ter 5)
sudo kubectl get deployment frontend
sudo kubectl get pods -l app=frontend
```

#### 4.4 Testar Conectividade Frontend → Backend

```bash
# Entrar em um pod do frontend
sudo kubectl exec -it <FRONTEND_POD> -- /bin/sh

# Testar acesso ao backend
wget -O- http://backend:8000/api/
```

---

## 📊 Decisões de Arquitetura

### Por que K3S?

- ✅ **Leve:** Usa menos recursos que K8S completo
- ✅ **Fácil:** Setup simples em minutos
- ✅ **Produção:** Certificado pela CNCF
- ✅ **Econômico:** Roda bem em t3.micro/small

### Por que 1 Master + 2 Workers?

- ✅ Atende requisito "mínimo 2 nós"
- ✅ Master isolado (boas práticas)
- ✅ Workers distribuem carga
- ✅ Econômico (~$30/mês)

### Por que Docker Hub?

- ✅ Fácil acesso dos nós EC2
- ✅ Não precisa registry privado
- ✅ Sem custos adicionais
- ✅ Imagens públicas facilitam deploy

### Por que NodePort ao invés de LoadBalancer?

- ✅ **LoadBalancer na AWS custa extra** ($18/mês)
- ✅ NodePort é grátis e suficiente para academia
- ✅ Acesso direto via IP público
- 💡 Pode adicionar LoadBalancer depois se necessário

### Recursos por Pod

**Backend (5 réplicas):**
- Request: 256Mi RAM, 250m CPU
- Limit: 512Mi RAM, 500m CPU
- Total cluster: ~1.25Gi RAM, 1.25 CPU

**Frontend (5 réplicas):**
- Request: 256Mi RAM, 250m CPU
- Limit: 512Mi RAM, 500m CPU
- Total cluster: ~1.25Gi RAM, 1.25 CPU

**PostgreSQL (1 réplica):**
- Request: 256Mi RAM, 250m CPU
- Limit: 512Mi RAM, 500m CPU

**Total necessário:** ~3Gi RAM, 3 CPU
**Cluster disponível:** 4Gi RAM, 6 vCPU ✅

---

## 🔧 Troubleshooting

### Pods em CrashLoopBackOff

```bash
# Ver logs
sudo kubectl logs <POD_NAME>

# Ver eventos
sudo kubectl describe pod <POD_NAME>

# Problemas comuns:
# - Backend: banco não está pronto
# - Frontend: variável de ambiente errada
```

### Worker não conecta ao Master

```bash
# No Worker, verificar logs
sudo journalctl -u k3s-agent -f

# Verificar token e URL corretos
# Verificar security group libera porta 6443
```

### Imagem não baixa

```bash
# Verificar se imagem existe no Docker Hub
docker pull walber147/arkheion_backend:latest

# No master, forçar pull
sudo kubectl delete pod <POD_NAME>
```

### PostgreSQL não persiste dados

```bash
# Verificar PVC
sudo kubectl get pvc

# Verificar storage class
sudo kubectl get storageclass
```

---

## 📝 Comandos Úteis

```bash
# Ver tudo
sudo kubectl get all -A

# Reiniciar deployment
sudo kubectl rollout restart deployment/<NAME>

# Escalar réplicas
sudo kubectl scale deployment/<NAME> --replicas=5

# Port-forward para teste local
sudo kubectl port-forward svc/backend 8000:8000

# Entrar em um pod
sudo kubectl exec -it <POD_NAME> -- /bin/bash

# Ver uso de recursos
sudo kubectl top nodes
sudo kubectl top pods
```

---

## 🎓 Para a Apresentação

### Checklist Antes da Apresentação

- [ ] 3 nós (1 master + 2 workers) em Running
- [ ] 5 réplicas do backend rodando
- [ ] 5 réplicas do frontend rodando
- [ ] PostgreSQL funcionando com persistência
- [ ] Frontend acessível via browser
- [ ] Backend respondendo via API
- [ ] Demonstrar conexão frontend → backend → DB

### O que Mostrar

1. **Arquitetura AWS:**
   - 3 instâncias EC2
   - Security groups configurados

2. **Cluster K3S:**
   ```bash
   sudo kubectl get nodes
   sudo kubectl get pods -A
   sudo kubectl get svc -A
   ```

3. **Réplicas:**
   ```bash
   sudo kubectl get deployment
   sudo kubectl get pods -l app=backend
   sudo kubectl get pods -l app=frontend
   ```

4. **Conectividade:**
   ```bash
   sudo kubectl get svc
   # Mostrar ClusterIP do backend
   # Mostrar NodePort do frontend
   ```

5. **Aplicação Funcionando:**
   - Acessar via browser
   - Criar conta
   - Criar personagem
   - Mostrar dados persistidos

### Decisões para Explicar

1. **Por que K3S:** Leve, certificado, produção-ready
2. **Por que 3 nós:** Master isolado + 2 workers (HA)
3. **Por que 5 réplicas:** Alta disponibilidade e balanceamento
4. **Por que Services:** Abstração de rede interna do cluster
5. **Por que NodePort:** Acesso externo sem custo de LoadBalancer
6. **Por que Docker Hub:** Fácil deploy e atualização de imagens

---

## 💰 Gestão de Custos

### Custo Estimado (us-east-1)

- t3.small master: ~$15/mês
- t3.micro worker 1: ~$7.5/mês
- t3.micro worker 2: ~$7.5/mês
- **Total: ~$30/mês**

### Economia de $50

- Sobra: $20/mês
- Pode usar para:
  - LoadBalancer (se necessário)
  - RDS PostgreSQL (produção)
  - Snapshots/backups

### Dicas para Economizar

1. **Parar instâncias quando não usar**
   ```bash
   aws ec2 stop-instances --instance-ids <ID>
   ```

2. **Usar Reserved Instances** (não recomendado para labs temporários)

3. **Monitorar uso no Billing Dashboard**

---

## 🔐 Segurança

### Boas Práticas Implementadas

- ✅ SSH apenas com chave privada
- ✅ Security groups restritivos
- ✅ Secrets para senhas do banco
- ✅ ConfigMaps para configs não-sensíveis
- ✅ Network policies (pode adicionar)

### Melhorias Futuras

- [ ] Usar IAM roles ao invés de secrets
- [ ] Implementar ingress com TLS
- [ ] Adicionar network policies
- [ ] Implementar RBAC
- [ ] Usar AWS Secrets Manager

---

## 📚 Referências

- [K3S Documentation](https://docs.k3s.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EC2 Pricing](https://aws.amazon.com/ec2/pricing/)
- [Docker Hub](https://hub.docker.com/)

---

**Boa sorte na apresentação! 🚀**
