# 🎯 Guia Rápido - Atualizar IP AWS

## ⚡ Comando Rápido (Mais Usado)

Quando o IP mudar, execute **uma única linha**:

```bash
./update-ip.sh ec2-SEU-IP-AQUI.compute-1.amazonaws.com
```

**Exemplo com IP atual:**
```bash
./update-ip.sh ec2-3-81-166-171.compute-1.amazonaws.com
```

ou apenas com o IP:
```bash
./update-ip.sh 3.81.166.171
```

## 📋 Como Pegar as Informações da AWS

1. **Console AWS** → EC2 → Sua Instância
2. Copie um dos dois:
   - **DNS Público**: `ec2-X-X-X-X.compute-1.amazonaws.com` ⭐ **Recomendado**
   - **IP Público**: `X.X.X.X`

## 🔄 Fluxo Completo (Depois que o Lab Cair)

```bash
# 1. SSH no master
ssh -i sua-chave.pem ubuntu@NOVO-IP

# 2. Vai para o projeto
cd /caminho/para/Arkheion

# 3. Atualiza o IP/DNS (COPIE O DNS DO CONSOLE AWS)
./update-ip.sh ec2-3-81-166-171.compute-1.amazonaws.com

# 4. Rebuild e deploy
docker build -f Dockerfile.frontend.prod -t arkheion-frontend:latest .
cd aws
./deploy-app.sh
```

## ✅ O Que o Script Faz

1. ✅ Atualiza `frontend/.env.production`
2. ✅ Atualiza `Dockerfile.frontend.prod`
3. ✅ Cria backup `.bak` antes de modificar
4. ✅ Salva referência em `.env.aws`

## 🎁 Bônus: No Master AWS (Detecção Automática)

Se você rodar **dentro do master**, ele detecta tudo sozinho:

```bash
./update-ip.sh
# Pressione 'D' para usar DNS (recomendado)
# ou 'I' para usar IP
```

## 🚀 Vantagens do DNS vs IP

| Item | IP Direto | DNS Público |
|------|-----------|-------------|
| Estabilidade | ❌ Muda sempre | ✅ Atualizado pela AWS |
| Quando o lab cai | ❌ Quebra tudo | ✅ Funciona automático |
| Performance | ✅ Direto | ✅ Resolve rápido |
| Recomendação | ❌ | ⭐ **Use este!** |

## 📝 Exemplos de Uso

### Cenário 1: Lab acabou de subir
```bash
./update-ip.sh ec2-3-81-166-171.compute-1.amazonaws.com
```

### Cenário 2: Tem só o IP
```bash
./update-ip.sh 3.81.166.171
```

### Cenário 3: Rodando no master AWS
```bash
./update-ip.sh --use-dns
# Detecta e usa o DNS automaticamente
```

## 🆘 Troubleshooting

### Erro: "Permission denied"
```bash
chmod +x update-ip.sh
```

### Erro: Frontend não conecta
1. Verifique o security group na AWS (porta 30080)
2. Teste manualmente:
   ```bash
   curl http://SEU-DNS:30080/arkheion_api/
   ```

### Esqueci qual DNS/IP configurei
```bash
cat .env.aws
# ou
cat frontend/.env.production
```

## 🔗 Documentação Completa

Para detalhes técnicos, veja: [aws/IP-DINAMICO.md](IP-DINAMICO.md)
