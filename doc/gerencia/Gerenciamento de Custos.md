# Plano de Gerenciamento dos Custos - Projeto Arkheion

## Estimativa dos Pacotes

Esta planilha detalha a estimativa _bottom-up_ dos custos, listando o esforço e os recursos para cada pacote de trabalho.

| CÓDIGO    | PACOTE DE TRABALHO         | RECURSO PRINCIPAL | QTDE | FTE (MESES) | CUSTO MENSAL (R$/MÊS) | CUSTO TOTAL (R$) |
| :-------- | :------------------------- | :---------------- | :--- | :---------- | :-------------------- | :--------------- |
| 1.0       | Gestão Ágil (Daily/Sprint) | Scrum Master/GP   | 0,5  | 2           | R$ 8.000,00           | R$ 8.000,00      |
| 2.0       | Finalização da Nuvem       | Cloud Engineer    | 1    | 1           | R$ 7.000,00           | R$ 7.000,00      |
| 3.0       | Configuração Kubernetes    | DevOps Specialist | 1    | 1           | R$ 9.000,00           | R$ 9.000,00      |
| 4.0       | Pipeline CI/CD             | DevOps Specialist | 1    | 1           | R$ 9.000,00           | R$ 9.000,00      |
| 5.0       | Execução de Testes         | QA Tester         | 1    | 1           | R$ 6.000,00           | R$ 6.000,00      |
| 6.0       | Testes de Usabilidade      | UX Researcher     | 1    | 1           | R$ 3.000,00           | R$ 3.000,00      |
| 7.0       | Avaliação Empírica         | Pesquisador       | 1    | 1           | R$ 4.000,00           | R$ 4.000,00      |
| 8.0       | Encerramento/Paper         | Tech Writer       | 0,5  | 1           | R$ 5.000,00           | R$ 2.500,00      |
| INFRA     | Azure/AWS (Intenso)        | Créditos Cloud    | 1    | 2           | R$ 1.000,00           | R$ 2.000,00      |
| TOOLS     | Ferramentas de Teste       | Licenças          | 1    | 1           | R$ 1.000,00           | R$ 1.000,00      |
| **TOTAL** |                            |                   |      |             |                       | **R$ 51.500,00** |

---

<br><br>

## Consolidação

Resumo dos custos divididos por categoria.

| CATEGORIA                          |    VALOR (R$)    |
| :--------------------------------- | :--------------: |
| Custos Diretos                     |   R$ 51.500,00   |
| Custos Indiretos (Energia/Net)     |   R$ 2.000,00    |
| Reserva de Contingência (10%)      |   R$ 5.150,00    |
| **Linha de Base dos Custos (BAC)** | **R$ 58.650,00** |
| Reserva Gerencial (5%)             |   R$ 2.932,50    |
| **Orçamento Total do Projeto**     | **R$ 61.582,50** |

---

<br><br>

## EVM_Dados

Dados de entrada para o Gerenciamento de Valor Agregado ao longo dos 3 meses.

| MÊS | PV (PLANEJADO) R$ | EV (AGREGADO) R$ | AC (REAL) R$ |
| :-: | ----------------: | ---------------: | -----------: |
|  1  |      R$ 35.000,00 |     R$ 35.000,00 | R$ 32.000,00 |
|  2  |         23.650,00 |                - |            - |

| MÊS | PERCENTUAL |
| :-- | :--------: |
| 1   |    60%     |
| 2   |     -      |

---

<br><br>

## EVM_Resultados

Cálculo dos índices de desempenho e status do projeto.

| MÊS | PV (PLANEJADO) R$ | EV (AGREGADO) R$ | AC (REAL) R$ | SV  |    CV    | SPI | CPI  |
| :-: | :---------------: | :--------------: | :----------: | :-: | :------: | :-: | :--: |
|  1  |   R$ 35.000,00    |   R$ 35.000,00   | R$ 32.000,00 |  0  | 3.000,00 |  1  | 1,09 |
|  2  |     23.650,00     |        -         |      -       |  -  |    -     |  -  |  -   |

---

<br><br>

## EVM_Totais

Previsões finais baseadas no desempenho atual (Forecasting).

|   BAC (R$)   | SPI MÉDIO | CPI MÉDIO |   EAC (R$)   |  VAC (R$)   |
| :----------: | :-------: | :-------: | :----------: | :---------: |
| R$ 58.650,00 |     1     |   1,09    | R$ 53.809,00 | R$ 4.841,00 |

---

<br><br>

## Planilha1

Metadados gerais do arquivo e do projeto.

| INDICADOR | VALOR                 |     |
| :-------- | :-------------------- | :-- |
| **BAC**   | **R$ 100.000,00**     |     |
|           | _Status após 2 meses_ |     |
| **PV**    | R$ 50.000,00          |     |
| **EV**    | R$ 40.000,00          |     |
| **AC**    | R$ 45.000,00          |     |

<br>

|       SV       |      CV       | SVI | CPI  |      EAC      | VAC            |
| :------------: | :-----------: | :-: | :--: | :-----------: | -------------- |
| - R$ 10.000,00 | - R$ 5.000,00 | 0,8 | 0,89 | R$ 112.500,00 | - R$ 12.500,00 |

<br>

| SIGLA   | NOME                       | SIGNIFICADO           | FÓRMULA                                       |
| :------ | :------------------------- | :-------------------- | :-------------------------------------------- |
| **PV**  | Planned Value              | Valor Planejado       | Valor do trabalho que deveria estar concluído |
| **EV**  | Earned Value               | Valor Agregado        | Valor do trabalho realmente concluído         |
| **AC**  | Actual Cost                | Custo Real            | Valor gasto até o momento                     |
| **SV**  | Schedule Variance          | Variação de Prazo     | EV − PV                                       |
| **CV**  | Cost Variance              | Variação de Custo     | EV − AC                                       |
| **SPI** | Schedule Performance Index | Índice de Prazo       | EV ÷ PV                                       |
| **CPI** | Cost Performance Index     | Índice de Custo       | EV ÷ AC                                       |
| **EAC** | Estimate at Completion     | Estimativa no Término | BAC ÷ CPI                                     |
| **VAC** | Variance at Completion     | Variação no Término   | BAC − EAC                                     |

---

**Aprovado por:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ (Scrum Master)

**Data:** 28/11/2025
