# Caso de Teste - CDU018. Subir de Nível

**Resumo**: O usuário utiliza o sistema para subir o nível de seu personagem, podendo escolher entre subir o nível de uma classe existente ou adicionar uma nova classe (multiclasse).

## Histórico da Alteração

|    Data    | Versão | Descrição                   | Autor(es)       |
| :--------: | ------ | --------------------------- | --------------- |
| 28/10/2025 | 1.0    | Versão inicial do documento | Walber Ranniere |

## Testes Funcionais

### Fluxos Principais e Alternativos

| ID do Teste | Cenário de Teste                                                                                                  | Personagem (Nível, Classes)                                                      | Ação do Usuário                                                                 | Resultado Esperado                                                                                                                                                       | Resultado Obtido             | Situação |
| :---------- | :---------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------- | :------- |
| CT-NIV-01   | **Subir nível de classe única:** Testa o aumento de nível de um personagem com apenas uma classe.                 | Guerreiro Nível 5 (Guerreiro Nível 5)                                            | Clica em "Subir de Nível" e seleciona "Guerreiro".                              | O nível do personagem deve ir para **6** e o nível da classe Guerreiro deve ir para **6**. Vida e mana devem ser recalculadas automaticamente.                           | Nível 6, recálculo correto   | Aprovado |
| CT-NIV-02   | **Subir nível multiclasse:** Testa o aumento de nível de uma classe específica em personagem multiclasse.         | Bárbaro/Ranger Nível 8 (Bárbaro Nível 5, Ranger Nível 3)                         | Clica em "Subir de Nível" e seleciona "Ranger".                                 | O nível do personagem deve ir para **9** e o nível da classe Ranger deve ir para **4**. Bárbaro permanece nível 5.                                                       | Nível 9, Ranger 4, Bárbaro 5 | Aprovado |
| CT-NIV-03   | **Adicionar nova classe (multiclasse):** Testa a adição de uma segunda classe ao personagem.                      | Clérigo Nível 4 (Clérigo Nível 4)                                                | Clica em "Subir de Nível", seleciona aba "Adicionar Classe" e escolhe "Ladino". | O nível do personagem deve ir para **5**, deve ter Clérigo Nível 4 e Ladino Nível 1. Habilidades de Ladino nível 1 devem ser adicionadas automaticamente.                | Multiclasse adicionada       | Aprovado |
| CT-NIV-04   | **Habilidades automáticas:** Verifica se habilidades de classe são adicionadas automaticamente ao subir de nível. | Paladino Nível 1 (Paladino Nível 1)                                              | Clica em "Subir de Nível" e seleciona "Paladino".                               | O nível do personagem deve ir para **2**, nível de Paladino para **2**, e as habilidades de Paladino de nível 2 devem ser adicionadas automaticamente à ficha.           | Nível 2 com habilidades      | Aprovado |
| CT-NIV-05   | **Recálculo de perícias:** Verifica se as perícias são recalculadas após subir de nível.                          | Batedor Nível 3 (Batedor Nível 3)                                                | Clica em "Subir de Nível" e seleciona "Batedor".                                | O nível do personagem deve ir para **4**, e todas as perícias devem ter seus valores recalculados com o novo bônus de nível (+2 para +2).                                | Perícias recalculadas        | Aprovado |
| CT-NIV-06   | **Validação de dados inválidos (CI1):** Testa o comportamento quando dados inválidos são enviados.                | Mago Nível 2 (Mago Nível 2)                                                      | Tenta submeter formulário sem selecionar uma classe válida.                     | O sistema deve exibir mensagem de erro informando que é necessário selecionar uma classe válida. Nenhum valor deve ser alterado.                                         | Erro 400 - validação correta | Aprovado |
| CT-NIV-07   | **Classe já existente (CI2):** Testa tentativa de adicionar classe que o personagem já possui.                    | Arcano Nível 6 (Arcano Nível 6)                                                  | Clica em "Adicionar Classe" e tenta adicionar "Arcano" novamente.               | O sistema deve exibir mensagem de erro informando que a classe já está na ficha. Nenhuma alteração deve ser feita.                                                       | Erro de classe duplicada     | Aprovado |
| CT-NIV-08   | **Cálculo de vida e mana:** Verifica se vida e mana são recalculadas corretamente após subir de nível.            | Druida Nível 5, CON +2 (Druida Nível 5)                                          | Clica em "Subir de Nível" e seleciona "Druida".                                 | Vida máxima deve aumentar em (vida_por_nivel da classe Druida), mana máxima deve aumentar em (mana_por_nivel da classe Druida).                                          | Vida e mana recalculadas     | Aprovado |
| CT-NIV-09   | **Limite de nível (RN1):** Testa comportamento próximo ao limite máximo de nível.                                 | Guerreiro Nível 19 (Guerreiro Nível 19)                                          | Clica em "Subir de Nível" e seleciona "Guerreiro".                              | O nível do personagem deve ir para **20** e o nível da classe Guerreiro deve ir para **20**. Deve funcionar normalmente.                                                 | Nível 20 atingido            | Aprovado |
| CT-NIV-10   | **Personagem sem classes:** Testa cenário de erro onde personagem não possui classes.                             | Personagem Nível 1 (Sem classes cadastradas)                                     | Clica em "Subir de Nível".                                                      | O sistema deve exibir mensagem de erro informando que não há classes para subir de nível.                                                                                | Erro - sem classes           | Aprovado |
| CT-NIV-11   | **Cálculo multiclasse complexo:** Testa cálculos com personagem de múltiplas classes.                             | Guerreiro/Ladino/Mago Nível 12 (Guerreiro Nível 6, Ladino Nível 4, Mago Nível 2) | Clica em "Subir de Nível" e seleciona "Mago".                                   | O nível do personagem deve ir para **13**, Mago deve ir para nível **3**, outras classes permanecem inalteradas. Vida e mana recalculadas considerando todas as classes. | Multiclasse complexa OK      | Aprovado |
| CT-NIV-12   | **Cancelar operação:** Testa cancelamento da ação de subir de nível.                                              | Ranger Nível 7 (Ranger Nível 7)                                                  | Abre modal "Subir de Nível" e clica em "Cancelar" ou "X".                       | O modal deve fechar e nenhuma alteração deve ser feita no personagem. Valores permanecem inalterados.                                                                    | Cancelamento funcionando     | Aprovado |

<br>

### Regras de Negócio Identificadas

**RN1 - Limites de Nível:**

- O nível máximo de um personagem é 20
- O nível de uma classe individual pode chegar até 20
- A soma dos níveis de todas as classes determina o nível total do personagem

**RN2 - Multiclasse:**

- Um personagem pode ter múltiplas classes
- Ao subir de nível, o usuário deve escolher qual classe será aumentada
- Novas classes sempre começam no nível 1

**RN3 - Habilidades Automáticas:**

- Habilidades de classe do novo nível devem ser adicionadas automaticamente
- Habilidades duplicadas não devem ser adicionadas

**RN4 - Recálculos Automáticos:**

- Vida máxima deve ser recalculada considerando todas as classes
- Mana máxima deve ser recalculada considerando todas as classes
- Todas as perícias devem ter seus valores recalculados com o novo bônus de nível

**RN5 - Validações:**

- Deve existir pelo menos uma classe para subir de nível
- Não é possível adicionar uma classe que o personagem já possui
- Campos obrigatórios devem ser validados antes da submissão

<br>

## Mais detalhes dos casos de teste

_Os detalhes específicos dos casos de teste podem ser encontrados na documentação técnica do sistema, incluindo validações de API, fluxos de interface e tratamento de erros._
