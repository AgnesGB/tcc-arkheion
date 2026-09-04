#!/bin/bash

echo "🔍 Debug do Estado de Autenticação - Arkheion"
echo "=============================================="

# Verificar se o servidor está rodando
echo ""
echo "📡 Verificando servidores:"
echo "--------------------------"

# Backend (Django)
if curl -s http://localhost:8000/arkheion_api/ > /dev/null 2>&1; then
    echo "✅ Backend (Django) - Rodando em http://localhost:8000"
else
    echo "❌ Backend (Django) - NÃO está rodando em http://localhost:8000"
fi

# Frontend (Vue.js)
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo "✅ Frontend (Vue.js) - Rodando em http://localhost:5173"
else
    echo "❌ Frontend (Vue.js) - NÃO está rodando em http://localhost:5173"
fi

echo ""
echo "🔧 URLs de Configuração Atuais:"
echo "--------------------------------"

# Detectar URL atual do Codespaces
if [ -n "$CODESPACE_NAME" ]; then
    FRONTEND_URL="https://${CODESPACE_NAME}-5173.app.github.dev"
    BACKEND_URL="https://${CODESPACE_NAME}-8000.app.github.dev"
    CALLBACK_URL="${FRONTEND_URL}/auth/google/callback"
    
    echo "🌐 Ambiente: GitHub Codespaces"
    echo "📍 Frontend: $FRONTEND_URL"
    echo "📍 Backend: $BACKEND_URL"
    echo "📍 Google Callback: $CALLBACK_URL"
else
    echo "🖥️  Ambiente: Local"
    echo "📍 Frontend: http://localhost:5173"
    echo "📍 Backend: http://localhost:8000"
    echo "📍 Google Callback: http://localhost:5173/auth/google/callback"
fi

echo ""
echo "🔑 Testando Endpoint de Autenticação:"
echo "--------------------------------------"

# Testar endpoint de autenticação do backend
if [ -n "$CODESPACE_NAME" ]; then
    AUTH_URL="https://${CODESPACE_NAME}-8000.app.github.dev/arkheion_api/auth/"
else
    AUTH_URL="http://localhost:8000/arkheion_api/auth/"
fi

if curl -s "$AUTH_URL" > /dev/null 2>&1; then
    echo "✅ Endpoint de autenticação acessível: $AUTH_URL"
else
    echo "❌ Endpoint de autenticação NÃO acessível: $AUTH_URL"
fi

echo ""
echo "📋 Checklist para Resolução de Problemas:"
echo "==========================================="
echo ""
echo "1. ✅ Verificar se ambos os servidores estão rodando"
echo "2. ✅ Verificar URL no Google Cloud Console:"
echo "   - Vá para: https://console.cloud.google.com/"
echo "   - APIs e Serviços → Credenciais"
echo "   - Cliente OAuth: 275673449727-psjm101pfgjda3opri2pdt980ejunj8e.apps.googleusercontent.com"
if [ -n "$CODESPACE_NAME" ]; then
    echo "   - Adicione: $CALLBACK_URL"
else
    echo "   - Adicione: http://localhost:5173/auth/google/callback"
fi
echo ""
echo "3. ✅ Verificar logs do browser (F12 → Console):"
echo "   - Procure por erros ou logs começando com 🔑, ❌, ✅"
echo "   - Verifique se o token está sendo salvo no localStorage"
echo ""
echo "4. ✅ Verificar logs do backend:"
echo "   - No terminal do Django, procure por logs de OAuth"
echo ""
echo "5. ✅ Testar fluxo manual:"
echo "   - Abra o browser em modo incógnito"
echo "   - Acesse a página principal"
echo "   - Clique em 'Entrar'"
echo "   - Clique em 'Entrar com Google'"
echo "   - Complete o fluxo OAuth"
echo "   - Verifique se retorna e se o usuário fica logado"
echo ""
echo "💡 URLs importantes para debugging:"
if [ -n "$CODESPACE_NAME" ]; then
    echo "   - Frontend: $FRONTEND_URL"
    echo "   - Backend Admin: $BACKEND_URL/admin/"
    echo "   - API Root: $BACKEND_URL/arkheion_api/"
else
    echo "   - Frontend: http://localhost:5173"
    echo "   - Backend Admin: http://localhost:8000/admin/"
    echo "   - API Root: http://localhost:8000/arkheion_api/"
fi
