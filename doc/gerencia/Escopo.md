## 📄 Declaração de Escopo do Projeto

### 1. Título do Projeto

**Projeto de Melhoria da Interface e Implantação (Arkheion)**

### 2. Objetivo do Projeto

O objetivo principal deste projeto é melhorar a usabilidade e a experiência do usuário da interface existente do sistema Arkheion, garantindo sua qualidade técnica através de testes abrangentes e realizando a implantação final do produto em um ambiente de nuvem Azure configurado.

### 3. Entregáveis do Projeto (Escopo do Trabalho)

O projeto será concluído com a entrega e aprovação dos seguintes pacotes de trabalho principais, detalhados no Dicionário da EAP:

| Pacote Principal | Entregáveis Chave (Artefatos) |
| :--- | :--- |
| **1. Gerenciamento do Projeto (1.0)** | **Termo de Abertura**, **Plano de Gerenciamento**, **Relatórios de Acompanhamento** semanais/mensais e atas de **Reuniões de Status**. |
| **2. Definição e Planejamento (2.0)** | **Declaração do Escopo**, **EAP e Dicionário da EAP**, **Registro das Partes Interessadas** e **Cronograma de Marcos** do projeto. |
| **3. Desenvolvimento e Design (3.0)** | **Relatório de Avaliação Heurística**, **Interface Revisada** (com melhorias visuais e de responsividade implementadas) e **Registro das Alterações**. |
| **4. Qualidade e Testes (4.0)** | **Projeto dos Casos de Teste** (para módulo crítico), **Relatório de Testes Unitários e de Integração** e **Relatório de Qualidade** (incluindo avaliação heurística complementar pós-ajustes). |
| **5. Implantação (5.0)** | **Ambiente Azure Configurad**o, **Plano de Rollback**, **Deploy** do *Backend* e *Frontend* na nuvem, **Testes de Fumaça** em produção e **Manual de Instalação e Uso**. |
| **6. Encerramento da Fase (6.0)** | **Documentação Final** compilada, **Registro de Lições Aprendidas** e **Aprovação Formal** das entregas com o Orientador e Equipe. |

### 4. Limites do Escopo (Exclusões)

O projeto **NÃO** inclui as seguintes atividades e entregáveis, que estão fora de seu foco principal de *Melhoria de Interface e Implantação*:

* **Desenvolvimento de Novas Funcionalidades Core:** Não serão criadas novas funcionalidades de negócio ou requisitos não funcionais que não estejam diretamente relacionados à melhoria da interface (UX/UI) ou à implantação na Azure.
* **Suporte e Manutenção Contínua:** O projeto encerra-se com a **Aprovação Final da Implantação** (5.3.4) e o **Encerramento da Fase** (6.0). Atividades de manutenção, correções de bugs não críticos pós-encerramento ou suporte de produção de longo prazo não fazem parte deste escopo.
* **Teste de Carga e Desempenho Extensivos:** Os testes de desempenho estão limitados a testes básicos para validação da implantação (5.2.4), não incluindo um ciclo completo de testes de carga em escala.
* **Implantação em Outras Plataformas:** A implantação é estritamente no ambiente **Azure** (5.1 e 5.2). Outras plataformas de nuvem (AWS, GCP, etc.) estão excluídas.

### 5. Critérios de Aceitação do Projeto

O projeto será considerado bem-sucedido e encerrado formalmente quando todos os seguintes critérios forem atendidos:

1.  A **Interface do Usuário** for aprovada pelo Orientador e Cliente/Product Owner após o ciclo de **Revisão e Ajuste da Interface** (3.2.4) e validação dos **Testes Visuais e de Navegação** (3.2.3).
2.  O **Relatório Técnico de Resultados** dos testes (4.2.4) confirmar a cobertura e a correção das falhas nos módulos críticos, e o **Relatório Final Eureca** (4.3.4) atestar as melhorias de usabilidade.
3.  A **Implantação na Nuvem Azure** (5.2) for concluída e os **Testes de Fumaça** (5.3.1) forem aprovados, garantindo o funcionamento do sistema em ambiente de produção.
4.  A **Aprovação Formal das Entregas** (6.2) for obtida com as partes interessadas (Orientador e Equipe).