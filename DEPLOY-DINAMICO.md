# 🚀 Deploy Dinâmico - Sem Rebuild por Mudança de IP

## 🎯 O Problema Resolvido

Antes, toda vez que o IP da AWS mudava, era necessário:
1. ❌ Atualizar variáveis de ambiente
2. ❌ Rebuildar a imagem Docker
3. ❌ Aguardar o build completo (~5 minutos)
4. ❌ Fazer novo deploy

## ✅ Solução Implementada

O frontend agora **detecta automaticamente** o backend em runtime:

```typescript
// src/utils/config.ts
function getBackendUrl() {
  // Usa window.location.hostname para pegar o host atual
  // Frontend: http://ec2-X-X-X.compute-1.amazonaws.com:30173
  // Backend:  http://ec2-X-X-X.compute-1.amazonaws.com:30080
  return `${protocol}//${hostname}:30080/arkheion_api`;
}
```

**Vantagens:**
- ✅ Nenhum rebuild necessário quando o IP muda
- ✅ Funciona automaticamente em qualquer ambiente
- ✅ Desenvolvimento local continua funcionando
- ✅ Deploy mais rápido

## 📦 Como Fazer Deploy Agora

### 1. Build das Imagens (Uma Vez)

```bash
# Backend
docker build -f Dockerfile.prod -t arkheion-backend:latest .

# Frontend (não precisa de variáveis de ambiente!)
docker build -f Dockerfile.frontend.prod -t arkheion-frontend:latest .
```

### 2. Push para o Registry (se necessário)

```bash
docker tag arkheion-backend:latest seu-registry/arkheion-backend:latest
docker tag arkheion-frontend:latest seu-registry/arkheion-frontend:latest

docker push seu-registry/arkheion-backend:latest
docker push seu-registry/arkheion-frontend:latest
```

### 3. Deploy no Kubernetes

```bash
# Apenas aplique os manifestos
kubectl apply -f aws/manifests/

# Ou faça rollout restart se já estiver rodando
kubectl rollout restart deployment/frontend
kubectl rollout restart deployment/backend
```

## 🔄 Quando o IP Mudar

**Não faça nada!** 🎉

O frontend detectará automaticamente o novo IP quando o usuário acessar.

## 🧪 Testar Localmente

```bash
# Frontend detecta automaticamente localhost:8000 em dev
cd frontend
npm run dev

# Backend
cd arkheion
python manage.py runserver
```

## 📝 Arquivos Modificados

- ✅ `frontend/src/utils/config.ts` - Nova lógica de detecção dinâmica
- ✅ `frontend/src/services/auth.service.ts` - Usa config dinâmica
- ✅ `frontend/src/services/api.service.ts` - Usa config dinâmica
- ✅ `Dockerfile.frontend.prod` - Removidas variáveis de build-time
- ⚠️ `frontend/.env.production` - Ainda existe mas não é mais usada

## 🎨 Bonus: Timeouts Aumentados

Também aumentei os timeouts para conexões AWS:
- Auth: `10s` → `30s`
- API: `15s` → `45s`

Isso evita timeouts em conexões mais lentas.

## 🐛 Troubleshooting

### Frontend não encontra o backend

**Verifique:**
```bash
# No navegador, console:
# Você verá: "🔧 Backend URL (dinâmica): http://ec2-X-X-X:30080/arkheion_api"
```

### Erro CORS

Certifique-se que o backend permite o hostname correto:
```python
# arkheion/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    # Adicione o padrão AWS:
]
CORS_ALLOW_ALL_ORIGINS = True  # Para AWS
```

### Porta 30080 não responde

Verifique o Security Group da AWS:
- EC2 → Security Groups
- Adicionar Inbound: Custom TCP, Port 30080, Source 0.0.0.0/0
