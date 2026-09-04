# Plano de Gerenciamento dos Riscos: Projeto Arkheion

**Disciplina:** Gerência de Projetos

**Entrega:** 12 de Dezembro

**Foco:** Gerenciar Riscos da Fase 2 (DevOps e Validação Empírica)

---

### **1. Estrutura de Custos da Reserva**

| Item de Custo                     | Valor Total (R$) | Observação                                                                          |
| :-------------------------------- | :--------------- | :---------------------------------------------------------------------------------- |
| **Reserva de Contingência**       | **R$ 3.000,00**  | Alocada para cobrir custos de tempo, retrabalho ou migrações (como a Azure -> AWS). |
| **Linha de Base de Custos (BAC)** | R$ 144.000,00    | Orçamento total simulado (conforme o Exercício de EVM).                             |

---

### **2. Lista de Riscos**

| ID      | Risco Identificado                                                    | Área       | Impacto Potencial                                                     | Status Atual     |
| :------ | :-------------------------------------------------------------------- | :--------- | :-------------------------------------------------------------------- | :--------------- |
| **R01** | **Compressão da Fase de Correção** (Prazos)                           | Cronograma | Atraso na entrega final e necessidade de _overtime_ (uso da Reserva). | **Monitorado**   |
| **R02** | **Rejeição Subjetiva da Interface** (Qualidade)                       | Escopo     | Retrabalho extenso e não planejado (uso da Reserva).                  | **Monitorado**   |
| **R03** | **Falha Crítica na Configuração Azure**                               | Técnico    | Tempo e recursos desperdiçados na migração (custo já absorvido).      | **Resolvido**    |
| **R04** | **Vazamento de Escopo (Scope Creep)**                                 | Escopo     | Adição de funcionalidades não previstas (uso da Reserva).             | **Dormente**     |
| **R05** | **Dificuldades na integração Frontend/Backend** (Histórico - Etapa 1) | Técnico    | Atraso no desenvolvimento.                                            | **Resolvido**    |
| **R06** | **Indisponibilidade de um membro da equipe** (Histórico - Etapa 1)    | Recursos   | Sobrecarga do time.                                                   | **Não ocorrido** |

> **Legenda dos Status:**
>
> - **Monitorado**: Risco está sendo acompanhado regularmente, com ações preventivas em andamento.
> - **Resolvido**: Risco foi eliminado ou não representa mais ameaça ao projeto.
> - **Dormente**: Risco identificado, mas atualmente inativo ou com baixa probabilidade de ocorrência.
> - **Não ocorrido**: Risco previsto, mas não se materializou até o momento.

---

### **3. Análise Qualitativa dos Riscos**

|   ID    | Probabilidade (P) | Impacto (I) | Nota (PxI) | Prioridade | Classificação (Regra 20/60/20) |
| :-----: | :---------------: | :---------: | :--------: | :--------: | :----------------------------- |
| **R01** |     3 (Alto)      |  3 (Alto)   |   **9**    |  **ALTA**  | **Top 20% (Crítico)**          |
| **R03** |     2 (Médio)     |  3 (Alto)   |   **6**    | **MÉDIA**  | **Faixa dos 60%**              |
| **R02** |     2 (Médio)     |  2 (Médio)  |   **4**    | **MÉDIA**  | **Faixa dos 60%**              |
| **R05** |     2 (Médio)     |  3 (Alto)   |   **6**    | **MÉDIA**  | **Faixa dos 60%**              |
| **R06** |     1 (Baixo)     |  2 (Médio)  |   **2**    | **BAIXA**  | **Bottom 20% (Observável)**    |
| **R04** |     1 (Baixo)     |  1 (Baixo)  |   **1**    | **BAIXA**  | **Bottom 20% (Observável)**    |

---

### **4. Estratégia de Tratamento dos Riscos**

| ID      | Estratégia (Tipo)     | Plano de Tratamento (Prevenção / Mitigação)                                                                                                                                                        | Plano de Contingência (Ação Pós-Risco)                                                                                                                                                                                   |
| :------ | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R01** | **Mitigar**           | Iniciar a Avaliação Heurística de forma **paralela** e adiantada para garantir tempo de correção.                                                                                                  | Se o atraso for inevitável, usar a **Reserva de Contingência (R$ 3.000)** para cobrir _overtime_ ou solicitar formalmente um Pedido de Mudança de prazo.                                                                 |
| **R03** | **Aceitar/Contornar** | **Registro Histórico:** O plano de **"Deploy de Teste" na Azure foi ignorado** devido à falha percebida. O tempo de planejamento foi realocado para a configuração da nova nuvem.                  | **Ação Executada:** Foi realizada a **migração imediata** para a AWS (ou outra plataforma) e a implantação foi bem-sucedida, **encerrando o risco**.                                                                     |
| **R02** | **Prevenir**          | Formalizar o uso das **10 Heurísticas de Nielsen** no Plano de Qualidade como padrão de aceite técnico, removendo a subjetividade do critério.                                                     | Apresentar o **Relatório Técnico Heurístico** como prova da qualidade, e escalar a decisão de aprovação ao patrocinador/professores avaliadores.                                                                         |
| **R04** | **Aceitar**           | Reforçar o limite do **"Desenvolvimento de Novas Funcionalidades Core"** em todas as reuniões de _Sprint Review_.                                                                                  | **Utilizar a Reserva de Contingência (R$ 3.000)** para absorver o custo de tempo do retrabalho em caso de vazamento de escopo inevitável.                                                                                |
| **R05** | **Mitigar/Encerrado** | **Registro Histórico (Etapa 1):** Estabelecer pontos de integração bem definidos entre Frontend (Vue.js) e Backend (Django), documentar APIs com Swagger, realizar testes de integração contínuos. | **Ação Executada:** Problemas de integração foram **identificados e resolvidos** durante a Etapa 1. Lições aprendidas foram documentadas e aplicadas para prevenir reincidência na Fase 2.                               |
| **R06** | **Aceitar/Monitorar** | **Registro Histórico (Etapa 1):** Manter documentação clara de responsabilidades, distribuição equilibrada de tarefas, conhecimento compartilhado através de pair programming e code reviews.      | **Ação de Contingência:** Em caso de indisponibilidade, redistribuir tarefas entre membros restantes da equipe, usar a **Reserva de Contingência** para _overtime_ se necessário, ou solicitar extensão de prazo formal. |
