# Caso de Teste - CDU014. Utilizar Perícia

**Resumo**: O usuário interage com as perícias de sua ficha para visualizar e modificar seus bônus totais.

## Histórico da Alteração

|    Data    | Versão | Descrição                   | Autor(es)               |
| :--------: | ------ | --------------------------- | ----------------------- |
| 29/09/2025 | 1.0    | Versão inicial do documento | Lucas Pinheiro da Costa |

## Testes Funcionais

### Fluxos Principais e Alternativos

| ID do Teste | Cenário de Teste                                                                                             | Perícia (Requer Treino?) | Personagem (Nível, Atributo)   | Ação do Usuário                               | Resultado Esperado                                                                                                                | Resultado Obtido                   | Situação |
| :---------- | :----------------------------------------------------------------------------------------------------------- | :----------------------- | :----------------------------- | :-------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- | :------- |
| CT-PER-01   | **Cálculo de perícia comum:** Verifica o cálculo base de uma perícia que não exige treinamento.              | Atletismo (Não)          | Nível 10, Força 14 (+2 mod)    | Visualiza o valor da perícia.                 | O `valor_calculado` deve ser **7**. (5 de nível + 2 de atributo).                                                                 | Valor calculado = 7                | Aprovado |
| CT-PER-02   | **Treino, não obrigatório, de perícia:** Testa o bônus de treino em uma perícia comum.                       | Atletismo (Não)          | Nível 10, Força 14 (+2 mod)    | Marca a caixa "Treinado".                     | O `valor_calculado` deve ser atualizado instantaneamente para **11**. (7 do cálculo base + 4 de bônus de treino).                 | Valor calculado = 11 com treino    | Aprovado |
| CT-PER-03   | **Cálculo de perícia obrigatória:** Verifica o cálculo de uma perícia que exige treinamento e está treinada. | Ladinagem (Sim)          | Nível 4, Destreza 16 (+3 mod)  | Visualiza o valor da perícia (já treinada).   | O `valor_calculado` deve ser **7**. (2 de nível + 3 de atributo + 2 de bônus de treino).                                          | Valor calculado = 7                | Aprovado |
| CT-PER-04   | **Uso de perícia obrigatória sem treino (CI1):** Garante que o valor da perícia é zerado.                    | Ladinagem (Sim)          | Nível 4, Destreza 16 (+3 mod)  | Desmarca a caixa "Treinado".                  | O `valor_calculado` deve ser atualizado instantaneamente para **0**. Todos os outros bônus devem ser ignorados.                   | Valor calculado = 0 sem treino     | Aprovado |
| CT-PER-05   | **Inserir bônus adicional válido:** Testa a reatividade da UI com um bônus positivo.                         | Percepção (Não)          | Nível 8, Sabedoria 12 (+1 mod) | Digita "5" no campo de bônus adicional.       | O `valor_calculado` (inicialmente 5) deve ser atualizado instantaneamente para **10**. (4 de nível + 1 de atributo + 5 de bônus). | Valor calculado = 10 com bônus     | Aprovado |
| CT-PER-06   | **Inserir bônus adicional negativo:** Testa a reatividade da UI com uma penalidade.                          | Percepção (Não)          | Nível 8, Sabedoria 12 (+1 mod) | Digita "-2" no campo de bônus adicional.      | O `valor_calculado` (inicialmente 5) deve ser atualizado instantaneamente para **3**. (4 de nível + 1 de atributo - 2 de bônus).  | Valor calculado = 3 com penalidade | Aprovado |
| CT-PER-07   | **Deixar bônus adicional vazio:** Testa o comportamento do sistema ao limpar o campo de bônus.               | Percepção (Não)          | Nível 8, Sabedoria 12 (+1 mod) | Apaga o conteúdo do campo de bônus adicional. | O `valor_calculado` deve ser recalculado como se o bônus adicional fosse **0**. O sistema não deve quebrar.                       | Sistema trata como 0               | Aprovado |
| CT-PER-08   | **Inserir bônus adicional inválido (CV5):** Testa o tratamento de erro para entradas não numéricas.          | Percepção (Não)          | Nível 8, Sabedoria 12 (+1 mod) | Digita "abc" no campo de bônus adicional.     | O `valor_calculado` deve ser recalculado como se o bônus adicional fosse **0**. O sistema não deve quebrar.                       | Sistema trata entrada inválida     | Aprovado |

<br>

## Mais detalhes dos casos de teste

_Acesse o arquivo_ **[Detalhamento_CT-CDU014.pdf](detalhamento-testes/Detalhamento_CT-CDU014.pdf)**
