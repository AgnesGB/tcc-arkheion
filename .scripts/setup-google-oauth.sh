#!/bin/bash

# Script para configurar URLs de redirecionamento do Google OAuth
# Para uso em ambientes Codespaces onde as URLs mudam dinamicamente

echo "🔧 Configuração do Google OAuth para Codespaces"
echo "==============================================="

# Detectar URL atual do Codespaces
if [ -n "$CODESPACE_NAME" ]; then
    CURRENT_URL="https://${CODESPACE_NAME}-5173.app.github.dev"
    CALLBACK_URL="${CURRENT_URL}/auth/google/callback"
    
    echo "📍 Detectado ambiente Codespaces:"
    echo "   Frontend URL: $CURRENT_URL"
    echo "   Callback URL: $CALLBACK_URL"
else
    echo "⚠️  Não foi detectado ambiente Codespaces"
    echo "   Usando configuração local padrão"
    CURRENT_URL="http://localhost:5173"
    CALLBACK_URL="${CURRENT_URL}/auth/google/callback"
fi

echo ""
echo "📋 URLs que precisam ser registradas no Google Cloud Console:"
echo "============================================================"
echo ""
echo "1. Acesse: https://console.cloud.google.com/"
echo "2. Vá em 'APIs e Serviços' → 'Credenciais'"
echo "3. Encontre o Cliente OAuth 2.0: 275673449727-psjm101pfgjda3opri2pdt980ejunj8e.apps.googleusercontent.com"
echo "4. Adicione estas URLs na seção 'URIs de redirecionamento autorizados':"
echo ""
echo "   ✅ $CALLBACK_URL"
echo ""
echo "5. Para development local, também adicione:"
echo "   ✅ http://localhost:5173/auth/google/callback"
echo ""
echo "💡 Dica: Para facilitar o development, você pode adicionar um padrão mais amplo:"
echo "   ✅ https://*.app.github.dev/auth/google/callback"
echo "   (Isso permitirá qualquer URL do GitHub Codespaces)"
echo ""
echo "⚡ URLs já configuradas no código:"
echo "   - Frontend: Detecção automática da URL atual"
echo "   - Backend: Aceita redirect_uri dinâmico"
echo ""
echo "🔍 Status atual:"
echo "   Frontend URL configurada: $(echo "$CURRENT_URL" | cut -c1-50)..."
echo "   Backend pronto para: URLs dinâmicas"
echo ""
echo "✅ Após adicionar as URLs no Google Cloud Console, o login com Google funcionará!"
