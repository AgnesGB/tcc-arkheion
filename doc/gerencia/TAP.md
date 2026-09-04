# **TERMO DE ABERTURA DO PROJETO (TAP)**

## Histórico da revisão

|    Data    | Versão | Descrição                    | Autor(es)               |
| :--------: | :----- | :--------------------------- | :---------------------- |
| 19/09/2025 | 1.0    | Construção do TAP            | Lucas Pinheiro da Costa |
| 23/10/2025 | 1.1    | Edição e formalização do TAP | Lucas Pinheiro e Agnes Barbosa |
| 25/11/2025 | 2.0    | Atualização para a Fase 2 (DevOps, Testes Avançados e Avaliação Empírica) | Lucas Pinheiro |

### **1. Identificação do projeto**

**Nome do projeto:** Arkheion – Fase 2: automação, qualidade e validação empírica
**Patrocinador (Product Owner):** Luan Gonçalves Barbosa
**Gerente do projeto (Scrum Master):** Agnes Gonçalves Barbosa

---

### **2. Justificativa do projeto**

<!-- ADICIOANAR A NECESSIDADE DE TERMINAR A IMPLANTAÇÃO EM NUVEM DO QUE FICOU PENDENTE NA ETAPA 01 -->

O projeto Arkheion entra em uma nova fase de maturidade. Após a melhoria da interface e a implantação inicial em IaaS (Máquina Virtual), faz-se necessário finalizar sua implantação definitiva em ambiente de produção na nuvem (usando Azure e/ou AWS), e elevar o nível de engenharia de software aplicada ao sistema.

A necessidade atual exige a migração de uma implantação manual para uma orquestração de contêineres escalável (Kubernetes) e a automação dos processos de entrega (CI/CD), garantindo agilidade e confiabilidade nas atualizações.

Além disso, para validar academicamente e tecnicamente a solução, é imperativo realizar uma bateria de testes formais (funcionais, não-funcionais e de usabilidade) e conduzir uma avaliação empírica rigorosa para coletar dados quantitativos e qualitativos sobre a eficácia do sistema junto aos usuários finais.

---

### **3. Objetivos do projeto**

**Objetivo geral:**
Implementar rotinas de DevOps avançado, assegurar a qualidade do software através de testes abrangentes e validar a eficácia do sistema Arkheion através de métodos empíricos formais.

**Objetivos específicos:**

* Elaborar cronograma detalhado (Gantt/PERT), matriz de riscos e planilha orçamentária;
* Finalizar a implantação da aplicação em ambiente de produção na Azure e/ou AWS, validando seu funcionamento. 
* Implementar pipeline de CI/CD (Azure DevOps ou GitHub Actions) e realizar deploy em cluster Kubernetes (AKS);
* Planejar e executar testes de API, Funcionais e Não-funcionais;
* Preparar artefatos e conduzir testes de usabilidade com usuários reais;
* Definir e aplicar método formal (experimento controlado ou estudo de caso) para validação científica do sistema.

---

### **4. Premissas**

* Acesso concedido aos serviços avançados da Azure (AKS, Container Registry) e/ou da AWS (Amazon Elastic Kubernetes Service (EKS), AWS CodePipeline) com créditos suficientes;
* Disponibilidade de uma base de voluntários (jogadores/mestres de RPG) para os testes de usabilidade e avaliação empírica;
* A equipe possui ou adquirirá o conhecimento necessário em orquestração de contêineres (Kubernetes) dentro do prazo;
* O código-fonte atual está estável o suficiente para suportar a automação de pipelines.

---

### **5. Restrições**

* **Prazo:** todas as atividades devem ser concluídas até o final do 2º bimestre do semestre 2025.2;
* **Orçamento:** restrito aos créditos acadêmicos da Azure/AWS e ferramentas gratuitas/open-source; deve haver controle rigoroso dos custos simulados e reais;
* **Escopo:** o deploy deve ser containerizado e orquestrado (não apenas em VM);
* **Recursos Humanos:** a avaliação empírica deve seguir rigor científico formal.

---

### **6. Requisitos de alto nível**

* O sistema deve rodar em um cluster Kubernetes (AKS/EKS), com pods, services e ingress configurados;
* Todo commit na branch principal deve disparar testes e deploy automático (Pipeline CI/CD);
* O projeto deve apresentar Gráfico de Gantt detalhado (atividades, datas, duração, dependências e marcos) e Matriz de Riscos atualizada;
* Relatórios técnicos comprovando a execução de testes de API, carga (não-funcional) e usabilidade;
* Coleta e análise de dados reais de uso para o relatório empírico.

---

### **7. Principais riscos de alto nível**

| **Categoria** | **Risco** | **Impacto potencial** |
| :--- | :--- | :--- |
| Técnico | Complexidade na configuração do cluster Kubernetes (curva de aprendizado). | Atraso na entrega da infraestrutura e falha no deploy. |
| Financeiro | Consumo excessivo de créditos Azure/AWS pelo cluster. | Interrupção dos serviços antes da avaliação final. |
| Usuário | Baixa adesão de voluntários para os testes de usabilidade/empíricos. | Dados insuficientes para a validação científica/empírica. |
| Integração | Falhas no pipeline de CI/CD que bloqueiem novas versões. | Gargalo no desenvolvimento e correção de bugs. |
| Gestão | Cronograma subestimado para atividades de configuração complexa. | Perda de prazos dos marcos acadêmicos. |

---

### **8. Principais Stakeholders**

| **Papel** | **Nome / Responsável** |
| :--- | :--- |
| **Patrocinador / Product Owner** | Luan Gonçalves Barbosa |
| **Gerente de projeto / Scrum Master** | Agnes Gonçalves Barbosa |
| **Professores avaliadores** | Alan G. G. da Silva (Gerência de Projetos), Andre G. D. de Almeida, Francisco S. de Lima Filho, Gracon H. E. L. de Lima (Des. de Sistema Corporativo) e Marilia A. Freire (Teste de Software) |
| **Equipe executora (Desenvolvedores)** | Nathan Cavalcante de Lima, Lucas Pinheiro da Costa, João Victor da Fonseca Dionisio e Walber Ranniere da Silva Maia |
| **Usuários finais** | Mestres e jogadores de RPG de mesa |
| **Participantes do estudo** | Voluntários para avaliação empírica |


---

### **9. Marcos Principais**

| **Data** | **Marco** | **Descrição** |
| :--- | :--- | :--- |
| 25/11/2025 | Kick-off e aprovação do TAP 2.0 | Início oficial do novo projeto e aprovação do Termo de Abertura do Projeto (TAP). |
| 27/11/2025 | Implantação na Azure/AWS | Execução de Backend, Frontend e Banco de Dados em contêineres na nuvem, com correta comunicação dos serviços. |
| 28/11/2025 | Planejamento de custos | Planilha orçamentária (Gerenciamento de custos). |
| 01/12/2025 | Planejamento avançado | Gráfico de Gantt Detalhado e Matriz de Riscos.|
| 05/12/2025 | Infraestrutura e automação | Configuração do Cluster Kubernetes e Implementação do Pipeline CI/CD funcional. |
| 12/12/2025 | Ciclo de testes técnicos | Execução e relatórios de Testes de API, Funcionais e Não-funcionais (Carga/Stress). |
| 15/12/2025 | Validação com usuários | Realização dos Testes de Usabilidade e coleta de feedback. |
| 18/12/2025 | Avaliação empírica | Execução do experimento controlado/estudo de caso e coleta de dados. |
| 29/01/2026 | Entrega final e encerramento da fase 2 | Consolidação da documentação, entrega oficial e encerramento da fase do projeto. |


---

### **10. Autoridade do Gerente de Projeto**

Agnes Gonçalves Barbosa, na função de Gerente de Projeto / Scrum Master, possui autoridade para:

* Coordenar a alocação de tarefas técnicas (DevOps vs. Testes);
* Monitorar o consumo de orçamento da nuvem e solicitar paradas de serviço para economia;
* Cobrar os artefatos de documentação (Gantt, Riscos, Relatórios);
* Gerenciar o contato com os voluntários para os testes empíricos.

---

### **11. Aprovação**

Este documento formaliza o início da fase 2 do projeto Arkheion, focada em DevOps e Validação empírica.

| **Nome** | **Função** | **Assinatura / Data** |
| :--- | :--- | :--- |
| Luan Gonçalves Barbosa | Product Owner / Patrocinador | _____________________ |
| Agnes Gonçalves Barbosa | Gerente de Projeto / Scrum Master | _____________________ |
| Equipe de Desenvolvimento | Desenvolvedores | _____________________ |
