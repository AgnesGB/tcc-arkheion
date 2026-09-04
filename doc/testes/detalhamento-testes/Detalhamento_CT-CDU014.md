INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE  
CAMPUS NATAL CENTRAL \- CNAT  
DIRETORIA ACADÊMICA DE GESTÃO E TECNOLOGIA DA INFORMAÇÃO \- DIATINF  
CURSO DE TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS \- TADS

Lucas Pinheiro da Costa

**ATIVIDADE SOBRE ANÁLISE DO VALOR LIMITE PARA O CASO DE USO ‘UTILIZAR PERÍCIA’**

Atividade acadêmica, solicitada para a disciplina Teste de Software, ministrada pela professora Marília Aranha Freire, como pré-requisito de avaliação para a composição da nota bimestral.

Natal-RN  
SETEMBRO/2025

| INSTITUTO FEDERAL DO RN Campus Natal-Central                                 |
| ---------------------------------------------------------------------------- |
| **Disciplina:** Teste de Software                                            |
| **Professor(a):** Marília Aranha Freire                                      |
| **Discente:** Lucas Pinheiro da Costa **Matrícula:** 20231014040023          |
| **Curso:** TADS **Semestre:** 2025.2                                         |
| **Atividade:** Análise do Valor Limite para o caso de uso ‘Utilizar Perícia’ |

#### **1\. DADOS DE ENTRADA**

- **Identificador da Perícia:** A perícia específica que o usuário selecionará para o teste. Este é o principal dado de entrada durante o fluxo. Os tipos de perícia são cruciais para os testes, dividindo-se em:

  - Perícias comuns (utilizáveis por todos)

  - Perícias rotuladas como "Somente treinada"

Atualmente, as perícias categorizadas no sistema estão distribuídas da seguinte forma, abrangendo uma vasta gama de habilidades que os personagens podem utilizar: Acrobacia, Adestramento, Atletismo, Atuação, Cavalgar, Conhecimento, Cura, Diplomacia, Enganação, Fortitude, etc.

- **Estado de "Treinada":** Para cada perícia que exige treinamento por parte do personagem (caixa de marcação "Somente treinada"), a ficha do personagem deve conter um **indicador (booleano true/false)** se o personagem é treinado ou não naquela perícia.

- **Bônus adicional (opcional):** Esse campo serve para adicionar bônus temporários ou vindos de equipamentos e magias, por exemplo.

####

#### **2\. CONDIÇÕES DE VALIDAÇÃO**

As condições a seguir definem o sucesso ou falha da execução do caso de uso:

- **Validação do Fluxo Principal:** Quando uma perícia é válida e utilizável por aquele personagem, o sistema deve apresentar um campo na tela contendo o resultado final do cálculo daquela perícia. Este resultado será um valor numérico derivado da fórmula: (metade do nível do personagem \+ pontos do atributo-chave \+ bônus de treinamento, se aplicável). O teste será considerado bem-sucedido se o resultado for exibido corretamente no campo especificado da página.

- **Validação de reatividade da Interface (UI)**: Ao realizar uma ação no frontend (marcar uma perícia como "treinada" ou alterar o "bônus adicional"), o valor total da perícia na tela deve ser atualizado instantaneamente, antes mesmo da confirmação do backend.

- **Validação de persistência no backend:** Após uma alteração na UI e a respectiva chamada de API, os novos dados devem ser salvos corretamente no banco de dados. A confirmação é feita ao recarregar a página e verificar se os dados persistem.

- **Validação do Fluxo de Exceção UI:** Se uma perícia com requer_treino \= true for marcada como não treinada na interface, o seu valor_calculado exibido deve ser imediatamente definido como 0\.

#### **3\. CLASSES DE EQUIVALÊNCIA**

##### **Classes Válidas (CV)**

- **CV1:** Utilizar uma **perícia que não exige treinamento**

  - _Cenário:_ O sistema calcula automaticamente o valor da perícia.

  - _Resultado Esperado:_ O valor calculado é exibido em um campo da tela para conhecimento do usuário

- **CV2:** Personagem **treinado** em perícia **sem obrigatoriedade**.

  - _Cenário:_ O usuário marca a caixa "treinado" para uma perícia que não o exige (ex: Atletismo).

  - _Resultado Esperado:_ O sistema deve reconhecer a ação e adicionar o bônus de treinamento correspondente ao nível do personagem no cálculo do valor final da perícia.

- **CV3:** Utilizar uma **perícia que exige treinamento** (`requer_treino = true`) e na qual o personagem **é treinado** (`treinado = true`).

  - _Cenário:_ O sistema calcula automaticamente o valor da perícia considerando o acréscimo do bônus de treinamento.

  - _Resultado Esperado:_ O valor calculado é exibido em um campo da tela para conhecimento do usuário.

- **CV4:** **Alterar** o estado de uma **perícia por meio da interface**.

  - _Cenário:_ Marcar/desmarcar a caixa de "treinado" ou inserir um número inteiro válido no campo de "bônus adicional".

  - _Resultado Esperado:_ A UI é atualizada instantaneamente e a alteração é enviada ao backend.

- **CV5:** **Inserir dados** de formato **inválido** no campo "bônus adicional".

  - _Cenário:_ Digitar um texto (ex: "abc") no campo de bônus.

  - _Resultado Esperado:_ O sistema deve tratar a entrada de forma graciosa, provavelmente interpretando-a como 0, graças ao `parseInt()` no código do componente `PericiaItem.vue`. O sistema não deve quebrar.

##### **Classes Inválidas (CI)**

- **CI1:** Tentar utilizar uma **perícia que exige treinamento** (`requer_treino = true`) mas na qual o personagem **não é treinado** (`treinado = false`).

  - _Cenário:_ O sistema atribui valor zero automaticamente para a perícia considerando tal condição.

  - _Resultado Esperado:_ O `valor_calculado` exibido deve ser 0\.

#### **4\. CASOS DE TESTE (ANÁLISE DO VALOR LIMITE)**

    Os casos de teste podem ser conferidos no arquivo ‘CT-CDU014.md’  (acessível me [https://github.com/tads-cnat/Arkheion/blob/main/doc/testes/CT-CDU014.md](https://github.com/tads-cnat/Arkheion/blob/main/doc/testes/CT-CDU014.md))
