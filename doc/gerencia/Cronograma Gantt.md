<!--  Converter as atividades em horas e ver como fica no gráfico de Gantt
      Usar o MS Project para o gráfico se o Mermaid não der certo -->
<!-- Analisar as sequências de atividades e dependências -->

```mermaid
gantt
  title Cronograma do Projeto 2.0 Arkheion
  dateFormat  YYYY-MM-DD

  section Iniciação
    Kickoff do projeto 2.0             :done, ini1, 2025-11-06, 1d
    Definição do escopo e premissas   :done, ini2, after ini1, 2d
    Aprovação TAP 2.0       :done, ini3, after ini2, 1d
    (Marco) Início oficial                 :milestone, m1, after ini3, 0d

  section Planejamento
    Cronograma detalhado           :done, plan1, after ini3, 3d
    Gerenciamento de Custos        :done, plan2, after ini3, 3d
    Gerenciamento de Riscos        :active, plan3, after plan1, 3d
    (Marco) Planejamento concluído         :milestone, m2, after plan3, 0d

  section DevOps e Infra
    Configuração da Nuvem                   :active, devops1, after m1, 4d
    Orquestração Kubernetes        :devops2, after devops1, 6d
    Pipeline CI/CD                 :devops3, after devops2, 4d
    (Marco) Ambiente K8s finalizado            :milestone, m3, after devops3, 0d

  section Desenvolvimento
    Design UI/UX                   :active, des1, after m2, 14d
    Banco de Dados PostegreSQL                 :done, db1, after devops1, 7d
    Backend API REST               :done, back1, after devops1,27d
    Frontend Node                      :active, front1, after m2, 27d
    (Marco) Dev Core finalizado            :milestone, m4, after front1, 0d

  section Qualidade
    Planejamento de testes         :qa1, after back1, 3d
    Testes API e Unitários         :qa2, after back1, 7d
    Testes Funcionais e de Carga      :crit, qa3, after front1, 7d
    Teste de Usabilidade           :crit, qa4, after front1, 4d
    Avaliacao Empirica             :crit, qa5, after qa4, 3d
    (Marco) QA finalizado           :milestone, m5, after qa4, 0d

  section Encerramento
    Implantação final              :end1, after qa5, 2d
    Relatório final e lições aprendidas       :end2, after end1, 1d
    (Marco) Projeto entregue com artefatos               :milestone, m6, after end2, 0d
```
