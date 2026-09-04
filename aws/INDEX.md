# 📚 Índice - Deploy AWS K3S Arkheion

## 🎯 Começo Rápido

**Quer começar agora?** → [QUICKSTART.md](QUICKSTART.md)

**Preparar apresentação?** → [APRESENTACAO.md](APRESENTACAO.md)

---

## 📁 Estrutura de Arquivos

```
aws/
├── README.md                    # 📖 Guia completo detalhado
├── QUICKSTART.md                # ⚡ Guia rápido (35 min)
├── APRESENTACAO.md              # 🎤 Roteiro de apresentação
├── INDEX.md                     # 📚 Este arquivo
│
├── setup-master.sh              # 🖥️ Script setup do master node
├── setup-worker.sh              # 🖥️ Script setup dos workers
├── deploy-app.sh                # 🚀 Script deploy da aplicação
│
└── manifests/                   # 📦 Manifestos K8S
    ├── README.md                # Guia dos manifestos
    ├── postgres-*.yaml          # PostgreSQL
    ├── backend-*.yaml           # Backend Django
    ├── frontend-*.yaml          # Frontend Vue.js
    └── frontend-service.yaml    # NodePort Service
```

---

## 📖 Guias por Objetivo

### 🎓 Para Fazer o Deploy

1. **[QUICKSTART.md](QUICKSTART.md)** - Início rápido em 6 passos
2. **[README.md](README.md)** - Guia completo com explicações detalhadas
3. **[manifests/README.md](manifests/README.md)** - Documentação dos manifestos

### 🎤 Para Apresentar

1. **[APRESENTACAO.md](APRESENTACAO.md)** - Roteiro completo da apresentação
   - Checklist pré-apresentação
   - Script com o que falar
   - Comandos prontos para copiar/colar
   - Respostas para perguntas comuns

### 🛠️ Para Executar

1. **[setup-master.sh](setup-master.sh)** - Instala K3S no master
2. **[setup-worker.sh](setup-worker.sh)** - Conecta workers ao cluster
3. **[deploy-app.sh](deploy-app.sh)** - Deploy completo da aplicação

---

## 🎯 Fluxo Recomendado

### Primeira Vez (Setup Completo)

1. Ler [README.md](README.md) para entender a arquitetura
2. Seguir [QUICKSTART.md](QUICKSTART.md) passo a passo
3. Verificar se tudo funcionou
4. Estudar [APRESENTACAO.md](APRESENTACAO.md) para apresentação

### Refazer Deploy

1. Executar scripts diretamente (já conhece o processo)
2. Consultar [QUICKSTART.md](QUICKSTART.md) para comandos rápidos

### Atualizar Aplicação

1. Build e push de novas imagens
2. `kubectl rollout restart deployment/backend`
3. `kubectl rollout restart deployment/frontend`

---

## 📊 Requisitos da Atividade

| Requisito | Status | Onde Está |
|-----------|--------|-----------|
| Cluster K8S real | ✅ | K3S instalado via `setup-master.sh` |
| Mínimo 2 nós | ✅ | 3 nós (1 master + 2 workers) |
| Distribuição de produção | ✅ | K3S certificado CNCF |
| VMs na nuvem | ✅ | AWS EC2 |
| Manifests YAML | ✅ | `aws/manifests/*.yaml` |
| 5 réplicas | ✅ | Backend e Frontend |
| Services | ✅ | ClusterIP + NodePort |
| Sistema funcionando | ✅ | http://PUBLIC_IP:30173 |

---

## 💡 Decisões Técnicas

### Por que K3S?
- ✅ Leve e rápido
- ✅ Certificado pela CNCF
- ✅ Produção-ready
- ✅ Econômico (roda em t3.micro)

### Por que 3 Nós?
- ✅ Atende requisito "mínimo 2"
- ✅ Master dedicado (boas práticas)
- ✅ Workers para carga de trabalho
- ✅ Cabe no orçamento (~$30/mês)

### Por que Docker Hub?
- ✅ Gratuito para imagens públicas
- ✅ Fácil acesso dos nós EC2
- ✅ Não precisa configurar registry privado
- ✅ CI/CD friendly

### Por que NodePort?
- ✅ Gratuito (LoadBalancer custa $18/mês)
- ✅ Suficiente para academia
- ✅ Acesso direto via IP público
- ✅ Pode migrar para LB depois

---

## 🔧 Comandos Essenciais

### Durante o Setup
```bash
# Master
sudo bash setup-master.sh

# Worker
sudo bash setup-worker.sh

# Verificar cluster
kubectl get nodes
```

### Durante o Deploy
```bash
# Deploy automático
./deploy-app.sh

# OU deploy manual
kubectl apply -f manifests/
```

### Durante a Apresentação
```bash
# Ver nós (3)
kubectl get nodes

# Ver deployments
kubectl get deployments

# Ver réplicas backend (5)
kubectl get pods -l app=backend

# Ver réplicas frontend (5)
kubectl get pods -l app=frontend

# Ver services
kubectl get svc
```

### Troubleshooting
```bash
# Logs de um pod
kubectl logs <POD_NAME>

# Detalhes de um pod
kubectl describe pod <POD_NAME>

# Reiniciar deployment
kubectl rollout restart deployment/<NAME>

# Ver eventos
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## 💰 Custos Estimados

| Recurso | Tipo | Custo/mês |
|---------|------|-----------|
| EC2 Master | t3.small | ~$15 |
| EC2 Worker 1 | t3.micro | ~$7.5 |
| EC2 Worker 2 | t3.micro | ~$7.5 |
| **Total** | | **~$30** |

**Sobra:** $20 do orçamento de $50

---

## 📚 Referências

- [K3S Documentation](https://docs.k3s.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Hub](https://hub.docker.com/u/walber147)

---

## 🆘 Suporte

### Problemas Comuns

**Worker não conecta:**
- Verificar security group permite tráfego
- Usar IP PRIVADO do master na URL
- Verificar token correto

**Pods em CrashLoopBackOff:**
```bash
kubectl logs <POD_NAME>
kubectl describe pod <POD_NAME>
```

**Aplicação não acessível:**
- Verificar security group libera porta 30173
- Testar no master: `curl http://localhost:30173`
- Verificar service: `kubectl get svc frontend`

### Documentação Adicional

- **Arquitetura detalhada:** [README.md](README.md) seção "Decisões de Arquitetura"
- **Troubleshooting completo:** [README.md](README.md) seção "Troubleshooting"
- **Comandos úteis:** [README.md](README.md) seção "Comandos Úteis"

---

## ✅ Checklist Final

Antes da apresentação, verifique:

- [ ] 3 instâncias EC2 rodando
- [ ] `kubectl get nodes` mostra 3 nós Ready
- [ ] Backend com 5 pods Running
- [ ] Frontend com 5 pods Running
- [ ] PostgreSQL com 1 pod Running
- [ ] Aplicação acessível no browser
- [ ] Consegue criar conta e personagem
- [ ] Dados persistem após refresh

---

**Tudo pronto para o deploy! 🚀**

Qualquer dúvida, consulte os arquivos de documentação acima.
