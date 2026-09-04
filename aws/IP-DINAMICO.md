# Solução para IP Dinâmico do AWS Lab

## O Problema
Toda vez que o laboratório AWS cai, o IP público muda e é necessário atualizar manualmente em vários arquivos do projeto.

## A Solução Implementada

### 🎯 Uso do DNS Público da AWS
Em vez de usar o IP diretamente, agora usamos o **DNS público da instância EC2**:
```
ec2-3-81-166-171.compute-1.amazonaws.com
```

**Vantagens:**
- O DNS é atualizado automaticamente pela AWS quando o IP muda
- Mais estável que o IP direto
- Funciona mesmo após reinicializações

### 🔧 Script de Atualização Automática

Criado o script `update-ip.sh` que:
1. **Detecta automaticamente** as informações se rodando na instância EC2
2. **Permite entrada manual** se rodando localmente
3. Atualiza todos os arquivos necessários:
   - `frontend/.env.production`
   - `Dockerfile.frontend.prod`
   - `.env.aws` (arquivo de referência)

## Como Usar

### Opção 1: Rodando no Master (Automático)
```bash
# No master AWS, o script detecta tudo automaticamente
./update-ip.sh
```

### Opção 2: Rodando Localmente (Manual)
```bash
# Localmente, você digita as informações
./update-ip.sh

# O script vai perguntar:
# - IP Público: 3.81.166.171
# - DNS Público: ec2-3-81-166-171.compute-1.amazonaws.com
# - Usar DNS ou IP? [Recomendado: DNS]
```

### Opção 3: Atualização Rápida com Valores Padrão
```bash
# Aceita todos os padrões com Enter
./update-ip.sh
# Pressione Enter 3 vezes (usa valores do último update)
```

## Onde as Informações Estão Configuradas

### Arquivos Atualizados pelo Script:
- ✅ `frontend/.env.production` - Variável de ambiente do Vite
- ✅ `Dockerfile.frontend.prod` - Build argument do Docker
- ✅ `.env.aws` - Arquivo de referência (não usado diretamente)

### Arquivos que Já Usam Detecção Automática:
- ✅ `aws/deploy-app.sh` - Detecta automaticamente via metadata service
- ✅ `aws/setup-master.sh` - Detecta automaticamente via metadata service

## Fluxo de Trabalho Recomendado

### Quando o Lab AWS Cair e Subir Novamente:

1. **Conecte no Master SSH**
   ```bash
   ssh -i sua-chave.pem ubuntu@NOVO-IP
   ```

2. **Navegue até o projeto**
   ```bash
   cd /caminho/para/Arkheion
   ```

3. **Execute o script de atualização**
   ```bash
   ./update-ip.sh
   ```

4. **Faça rebuild do frontend**
   ```bash
   docker build -f Dockerfile.frontend.prod -t arkheion-frontend:latest .
   ```

5. **Execute o deploy**
   ```bash
   cd aws
   ./deploy-app.sh
   ```

## Informações da Instância Atual

```
IP Público:    3.81.166.171
DNS Público:   ec2-3-81-166-171.compute-1.amazonaws.com
IP Privado:    172.31.39.17
DNS Privado:   ip-172-31-39-17.ec2.internal
Porta Backend: 30080
```

## Melhorias Futuras (Opcionais)

### 1. DNS Dinâmico Externo (Gratuito)
Usar serviços como **DuckDNS** ou **No-IP** que atualizam automaticamente:
- Configurar um domínio como: `arkheion.duckdns.org`
- Script no master atualiza o DNS automaticamente
- Nunca mais precisa mudar nada!

### 2. IP Elástico AWS (Pago)
- Alocar um IP Elástico que nunca muda
- Custo: ~$3.60/mês se instância desligada
- Gratuito se instância sempre ligada

### 3. Automação Completa
Adicionar ao `setup-master.sh` para executar automaticamente:
```bash
# No final do setup-master.sh
cd /caminho/para/Arkheion
./update-ip.sh
```

## Troubleshooting

### Script não detecta a instância EC2
**Problema:** Rodando localmente ou metadata service desabilitado

**Solução:** Digite manualmente as informações quando solicitado

### DNS não está resolvendo
**Problema:** DNS pode demorar alguns minutos para propagar

**Solução:** Use o IP temporariamente ou aguarde 2-5 minutos

### Frontend não conecta no backend
**Problema:** Pode ser firewall ou NodePort não exposto

**Solução:** 
```bash
# Verificar se o serviço está rodando
kubectl get svc frontend

# Verificar security group AWS permite porta 30080
```

## Contato e Suporte

Para dúvidas ou melhorias, consulte a documentação do projeto ou abra uma issue.
