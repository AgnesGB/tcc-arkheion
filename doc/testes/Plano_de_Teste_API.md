# Plano de Teste - Sistema Arkheion

**Projeto:** Arkheion - Sistema de Gerenciamento de Fichas de Personagem para Tormenta 20  
**Versão:** 1.0  
**Data:** 20 de Janeiro de 2026  
**Responsáveis:** Equipe Arkheion

---

## 1. Introdução

### 1.1. Objetivo do Documento

Este documento descreve o planejamento completo dos testes para o sistema Arkheion, incluindo estratégias, escopo, recursos, cronograma e critérios de aceite. O objetivo é garantir a qualidade, confiabilidade e usabilidade do sistema através de uma abordagem estruturada de testes.

### 1.2. Escopo do Sistema

O Arkheion é uma plataforma web para criação e gerenciamento de fichas de personagens do RPG de mesa Tormenta 20. O sistema permite que jogadores:

- Criem e gerenciem contas de usuário
- Criem, editem e excluam fichas de personagens
- Gerenciem atributos, perícias, habilidades e níveis
- Utilizem recursos de homebrew (conteúdo customizado)

### 1.3. Referências

- [Documento de Visão](../visao/doc-visao.md)
- [Casos de Uso](../cdu/cdu.md)
- [Casos de Teste CT-CDU001](CT-CDU001.md) - Criar Ficha
- [Casos de Teste CT-CDU006](CT-CDU006.md) - Login
- [Casos de Teste CT-CDU007](CT-CDU007.md) - Criar Conta
- [Casos de Teste CT-CDU014](CT-CDU014.md) - Perícias
- [Casos de Teste CT-CDU018](CT-CDU018.md) - Subir de Nível

---

## 2. Estratégia de Teste

### 2.1. Abordagem Geral

A estratégia de testes do Arkheion utiliza uma abordagem **híbrida**, combinando:

1. **Testes Unitários de API (Caixa-Preta)**
   - Testar endpoints da API REST isoladamente
   - Validar entradas, saídas e códigos HTTP
   - Verificar regras de negócio

2. **Testes de Integração**
   - Testar fluxos completos entre múltiplos componentes
   - Validar interação entre views, serializers e models

3. **Testes de Interface (Manual)**
   - Avaliação de usabilidade com usuários reais
   - Identificação de problemas de UX/UI

4. **Testes Não Funcionais**
   - Performance e carga (Locust - Não realizado)
   - Segurança (validações de entrada, autenticação)

### 2.2. Níveis de Teste

| Nível           | Descrição                               | Ferramenta       | Responsável     |
| --------------- | --------------------------------------- | ---------------- | --------------- |
| **Unitário**    | Testes de funções e métodos individuais | Django TestCase  | Desenvolvedores |
| **Integração**  | Testes de APIs e fluxos completos       | Django APIClient | Desenvolvedores |
| **Sistema**     | Testes end-to-end do sistema completo   | Manual/Cypress   | QA              |
| **Aceitação**   | Validação com usuários reais            | Manual           | Stakeholders    |
| **Performance** | Testes de carga e stress                | Locust           | QA              |

### 2.3. Técnicas de Teste

- **Particionamento de Equivalência:** Dividir dados de entrada em classes válidas e inválidas
- **Análise de Valor Limite:** Testar limites superior e inferior de campos
- **Tabelas de Decisão:** Validar combinações de condições
- **Testes de Estado:** Verificar transições de estado (ex: nível do personagem)
- **Testes Baseados em Risco:** Priorizar funcionalidades críticas (autenticação, criação de ficha)

---

## 3. Escopo de Testes

### 3.1. Funcionalidades Testadas

#### 3.1.1. Módulo de Autenticação

- **CDU006 - Logar Usuário**
  - Login com username/email
  - Validação de credenciais
  - Geração de tokens (Token e JWT)
  - Segurança (SQL injection, limites)

- **CDU007 - Criar Conta**
  - Registro de novos usuários
  - Validação de email e username
  - Validação de senhas
  - Prevenção de duplicação

#### 3.1.2. Módulo de Fichas de Personagem

- **CDU001 - Criar Ficha**
  - Criação com dados válidos
  - Validação de campos obrigatórios
  - Suporte a homebrew
  - Cálculos automáticos (vida, mana)

- **CDU002 - Visualizar Ficha**
  - Listagem de fichas do usuário
  - Detalhes de ficha específica
  - Autorização (não ver fichas de outros)

- **CDU003 - Editar Ficha**
  - Atualização de campos
  - Validações de dados

- **CDU004 - Excluir Ficha**
  - Deleção com autorização
  - Confirmação de exclusão

#### 3.1.3. Módulo de Perícias

- **CDU014 - Utilizar Perícias**
  - Cálculo de valores (nível + atributo + bônus)
  - Treino de perícias
  - Bônus de treino por faixa de nível
  - Perícias que requerem treino
  - Bônus adicionais positivos/negativos

#### 3.1.4. Módulo de Progressão

- **CDU018 - Subir de Nível**
  - Subir nível classe única
  - Subir nível multiclasse
  - Adicionar nova classe
  - Limite de nível (máx 20)
  - Recálculo de vida, mana e perícias

### 3.2. Funcionalidades NÃO Testadas (Fora do Escopo)

As seguintes funcionalidades **não serão testadas** nesta iteração:

**Módulos Não Implementados:**

- CDU005-009: Mesa de Jogo (criar, editar, excluir, convidar, remover)
- CDU012-013: Editar/Excluir conta de usuário
- CDU015: Alterar Mana ou Vida (apenas recálculo automático testado)
- CDU016-017: Bônus e treino de perícia (testado via CDU014)
- CDU019: Adicionar bônus de atributo
- CDU020: Gerenciar Habilidades
- CDU021-026: Ataques, Magias, Itens, Descrição, Monstros

**Integrações Externas:**

- Integração com Discord, Roll20, Owlbear Rodeo
- Compartilhamento de fichas

**Funcionalidades Avançadas:**

- Histórico de alterações
- Backup/Restore
- Exportação de fichas (PDF, JSON)

**Compatibilidade:**

- Navegadores legados (IE)

**Justificativa:** Funcionalidades listadas acima não estão implementadas ou não são prioritárias para a entrega atual.

---

## 4. Critérios de Aceitação e Saída

### 4.1. Critérios de Entrada

Para iniciar os testes, os seguintes critérios devem ser atendidos:

- Código-fonte estável e versionado (Git)
- Ambiente de desenvolvimento configurado
- Casos de teste documentados
- Base de dados de teste disponível

### 4.2. Critérios de Aceitação

Para que uma funcionalidade seja considerada **APROVADA**:

1. **Testes Funcionais:**
   - ≥ 95% dos casos de teste passando
   - Todos os fluxos principais funcionando
   - Validações de entrada implementadas

2. **Testes de API:**
   - 100% dos testes automatizados passando
   - Cobertura de código ≥ 75%
   - Todos os endpoints retornando status HTTP corretos

3. **Testes de Segurança:**
   - Autenticação/autorização funcionando
   - Validação de entrada contra SQL injection
   - Senhas armazenadas com hash

4. **Testes de Performance:**
   - Tempo de resposta < 1s para 90% das requisições
   - Suporte a ≥ 50 usuários simultâneos

5. **Testes de Interface:**
   - ≥ 80% de satisfação dos usuários
   - Problemas de gravidade ALTA resolvidos

### 4.3. Critérios de Saída

Os testes serão **ENCERRADOS** quando:

- Todos os critérios de aceitação forem atendidos
- Todos os bugs críticos/altos forem corrigidos
- Evidências de teste documentadas
- Relatório final de testes aprovado

---

## 5. Recursos

### 5.1. Recursos Humanos

| Função              | Responsabilidade                                 | Quantidade |
| ------------------- | ------------------------------------------------ | ---------- |
| **Desenvolvedores** | Criar e executar testes automatizados            | 5          |
| **Analista de QA**  | Planejar testes, revisar casos, gerar relatórios | 1          |
| **Usuários Beta**   | Participar de testes de usabilidade              | 4+         |

### 5.2. Recursos de Software

| Ferramenta                | Versão | Propósito                   |
| ------------------------- | ------ | --------------------------- |
| **Python**                | 3.12+  | Linguagem de programação    |
| **Django**                | 5.1+   | Framework web e testes      |
| **Django REST Framework** | 3.14+  | API e testes de API         |
| **PostgreSQL**            | 16+    | Banco de dados produção     |
| **SQLite**                | 3.x    | Banco de dados testes       |
| **Coverage.py**           | 7.6+   | Cobertura de código         |
| **Git/GitHub**            | -      | Versionamento               |
| **VS Code**               | -      | IDE                         |
| **Discord**               | -      | Testes remotos de interface |

### 5.3. Recursos de Hardware

- **Servidor de Desenvolvimento:** Dev Container (Linux Debian 12)
- **Banco de Dados:** PostgreSQL (localhost)
- **Navegadores:** Chrome, Firefox, Edge (versões recentes)

### 5.4. Ambiente de Testes

| Ambiente            | Descrição                         | Configuração          |
| ------------------- | --------------------------------- | --------------------- |
| **Desenvolvimento** | Máquina local dos desenvolvedores | SQLite in-memory      |
| **Testes**          | Ambiente dedicado para testes     | PostgreSQL de teste   |
| **Staging**         | Pré-produção                      | Docker compose (dev)  |
| **Produção**        | Ambiente final                    | Docker compose (prod) |

---

## 6. Tipos de Teste

### 6.1. Testes Funcionais

#### 6.1.1. Testes de API

**Objetivo:** Validar endpoints REST da API

**Técnica:** Caixa-preta, particionamento de equivalência

**Cobertura:**

- 5 CDUs implementados
- 97 testes automatizados
- 100% de sucesso

**Casos de Teste:**

- [CT-CDU001](CT-CDU001.md) - Criar Ficha (7 cenários)
- [CT-CDU006](CT-CDU006.md) - Login (10 cenários)
- [CT-CDU007](CT-CDU007.md) - Criar Conta (11 cenários)
- [CT-CDU014](CT-CDU014.md) - Perícias (8 cenários)
- [CT-CDU018](CT-CDU018.md) - Subir de Nível (12 cenários)

**Evidências:**

- [evidencias_execucao_testes.log](evidencias_execucao_testes.log)
- Código: `arkheion/backend/tests/test_api_*.py`

#### 6.1.2. Testes de Interface

**Objetivo:** Avaliar usabilidade e experiência do usuário

**Técnica:** Teste de usabilidade remoto (observação)

**Cobertura:**

- 6 participantes
- 12 tarefas avaliadas
- 17 problemas identificados (6 Alta, 7 Média, 4 Baixa gravidade)
- 50% satisfação "Fácil" ou superior

**Casos de Teste:**

- Avaliar fluxo de criação de conta
- Avaliar criação de ficha
- Avaliar gerenciamento de homebrews
- Avaliar gestão de perícias e atributos

**Evidências:**

- [Avaliação Empirica.md](../teste%20de%20interface/Avaliação%20Empirica.md)

### 6.2. Testes Não Funcionais

#### 6.2.1. Testes de Performance

**Objetivo:** Verificar tempos de resposta e capacidade do sistema

**Técnica:** Testes de carga com Locust

**Métricas:**

- Tempo de resposta médio
- Requisições por segundo (RPS)
- Taxa de erro
- Número de usuários simultâneos

**Cenários:**

- Carga normal: 10-20 usuários simultâneos
- Pico de carga: 50-100 usuários simultâneos
- Stress: > 100 usuários

**Evidências:**

- Relatórios HTML do Locust
- `arkheion/backend/load_tests/locustfile.py`

#### 6.2.2. Testes de Segurança

**Objetivo:** Identificar vulnerabilidades

**Cobertura:**

- Autenticação e autorização
- Validação de entrada (SQL injection)
- Hash de senhas
- Tokens seguros (JWT/Token)
- XSS (limitado)
- CSRF (limitado)

**Evidências:**

- Testes de SQL injection em CT-CDU006
- Validação de autorização em testes de API

#### 6.2.3. Testes de Cobertura

**Objetivo:** Medir quanto do código está coberto por testes

**Ferramenta:** Coverage.py

**Resultados:**

- **Cobertura Total:** 76%
- **Models:** 82%
- **Serializers:** 68%

**Meta:** ≥ 75% Atingida

**Evidências:**

- [coverage_report.txt](coverage_report.txt)
- [htmlcov/index.html](htmlcov/index.html)

---

## 7. Gerenciamento de Defeitos

### 7.1. Classificação de Severidade

| Severidade  | Descrição                              | Exemplo                       | Tempo de Correção |
| ----------- | -------------------------------------- | ----------------------------- | ----------------- |
| **Crítica** | Sistema inutilizável ou perda de dados | Não consegue fazer login      | Imediato (< 24h)  |
| **Alta**    | Funcionalidade principal quebrada      | Não calcula vida corretamente | 1-3 dias          |
| **Média**   | Funcionalidade secundária com problema | Label faltando em perícia     | 1 semana          |
| **Baixa**   | Problema cosmético ou de usabilidade   | Cor de botão pouco visível    | 2 semanas         |

### 7.2. Processo de Defeito

1. **Identificação:** Teste falha ou problema encontrado
2. **Registro:** Criar issue no GitHub com detalhes
3. **Classificação:** Atribuir severidade e prioridade
4. **Atribuição:** Designar desenvolvedor responsável
5. **Correção:** Implementar fix e criar teste de regressão
6. **Verificação:** Reexecutar teste para confirmar correção
7. **Fechamento:** Fechar issue após validação

### 7.3. Problemas Identificados

Veja seção detalhada no [Relatório de Testes](Relatorio_Testes_API.md#4-problemas-encontrados).

**Resumo:**

- **Interface:** 6 problemas (1 Alto, 4 Médio, 2 Baixo)
- **API:** 0 problemas críticos encontrados

---

## 8. Riscos

### 8.1. Riscos Técnicos

| Risco                                  | Probabilidade | Impacto | Mitigação                         |
| -------------------------------------- | ------------- | ------- | --------------------------------- |
| Falha de conexão com BD durante testes | Média         | Alto    | Usar SQLite in-memory para testes |
| Mudança de requisitos durante testes   | Baixa         | Médio   | Manter casos de teste atualizados |
| Bugs em dependências externas          | Baixa         | Alto    | Fixar versões no requirements.txt |
| Ambiente de teste instável             | Baixa         | Médio   | Usar Docker para padronizar       |
