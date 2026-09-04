# 🚀 Quick Start - Deploy Arkheion na AWS

## Resumo em 5 Passos

### 1️⃣ Criar Infraestrutura AWS (Console)

**Security Group `k3s-cluster`:**
- SSH (22) - My IP
- K3S API (6443) - 0.0.0.0/0
- HTTP (80) - 0.0.0.0/0
- HTTPS (443) - 0.0.0.0/0
- UDP (8472) - 10.0.0.0/8
- All Traffic - Source: k3s-cluster

**Key Pair:** `k3s-key.pem`

**EC2 Instances:**
- Master: t3.small, Ubuntu 22.04, 20GB, k3s-cluster
- Worker 1: t3.micro, Ubuntu 22.04, 15GB, k3s-cluster
- Worker 2: t3.micro, Ubuntu 22.04, 15GB, k3s-cluster

### 2️⃣ Setup Master

```bash
# SSH no master
ssh -i k3s-key.pem ubuntu@<MASTER_PUBLIC_IP>

# Baixar e executar script
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/setup-master.sh
sudo bash setup-master.sh

# SALVAR O TOKEN que aparecer no final!
```

### 3️⃣ Setup Workers

**Worker 1:**
```bash
# SSH no worker
ssh -i k3s-key.pem ubuntu@<WORKER1_PUBLIC_IP>

# Baixar script
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/setup-worker.sh

# Editar script com token e URL do master
nano setup-worker.sh

# Configurar:
# K3S_URL="https://<MASTER_PRIVATE_IP>:6443"
# K3S_TOKEN="<TOKEN_DO_MASTER>"
# WORKER_NAME="k3s-worker-1"

# Executar
sudo bash setup-worker.sh
```

**Repetir para Worker 2** (mudar WORKER_NAME para "k3s-worker-2")

### 4️⃣ Verificar Cluster

No master:
```bash
sudo kubectl get nodes
# Deve mostrar 3 nós Ready
```

### 5️⃣ Deploy Aplicação

```bash
# No master
mkdir -p ~/manifests
cd ~/manifests

# Baixar manifestos do PostgreSQL
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/postgres-pvc.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/postgres-configmap.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/postgres-secret.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/postgres-deployment.yaml  # Deployment + Service

# Baixar manifestos do Backend
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/backend-configmap.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/backend-secret.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/backend-deployment.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/frontend-configmap.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/frontend-deployment.yaml
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/manifests/frontend-service.yaml

# OU baixar script de deploy
cd ~
wget https://raw.githubusercontent.com/tads-cnat/Arkheion/homolog/aws/deploy-app.sh
chmod +x deploy-app.sh
./deploy-app.sh
```

### 6️⃣ Acessar Aplicação

```
http://<MASTER_PUBLIC_IP>:30173
```

---

## ⏱️ Tempo Estimado

- Criar infraestrutura AWS: **10 minutos**
- Setup cluster K3S: **15 minutos**
- Deploy aplicação: **10 minutos**
- **Total: ~35 minutos**

---

## 📊 Para a Apresentação

```bash
# 1. Mostrar nós
kubectl get nodes

# 2. Mostrar deployments
kubectl get deployments

# 3. Mostrar réplicas backend (5)
kubectl get pods -l app=backend

# 4. Mostrar réplicas frontend (5)
kubectl get pods -l app=frontend

# 5. Mostrar services
kubectl get svc

# 6. Acessar no browser
# http://<PUBLIC_IP>:30173
```

---

## 🆘 Problemas Comuns

**Worker não conecta:**
- Verificar security group
- Usar IP PRIVADO do master no K3S_URL
- Verificar token está correto

**Pods em CrashLoopBackOff:**
```bash
kubectl logs <POD_NAME>
kubectl describe pod <POD_NAME>
```

**Backend não inicia:**
- Aguardar PostgreSQL ficar pronto
- Ver logs: `kubectl logs -l app=backend`

---

**Documentação completa:** [aws/README.md](README.md)
