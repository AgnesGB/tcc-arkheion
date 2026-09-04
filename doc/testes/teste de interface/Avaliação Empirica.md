# Relatório Individual de Sessão de Teste de Usabilidade

**Projeto:** Arkheion

**Data:** 22/12/2025

**Modalidade:** Remoto

**Ferramenta utilizada:** Discord

## 2. Metodologia: Tarefas Solicitadas

Os participantes deveriam completar o seguinte fluxo de tarefas:

| Nº  | Tarefa                        | Objetivo                                                                 |
| --- | ----------------------------- | ------------------------------------------------------------------------ |
| 1   | Faça uma conta                | Validar clareza do onboarding e distinção entre "Entrar" e "Cadastrar"   |
| 2   | Faça um Homebrew              | Avaliar intuitividade do formulário e persistência na primeira tentativa |
| 3   | Acesse seus Homebrews         | Testar navegabilidade e visibilidade das abas principais                 |
| 4   | Faça uma ficha de personagem  | Validar fluxo principal e facilidade de iniciar a experiência central    |
| 5   | Adicionar treino nas perícias | Verificar compreensão da interface e aplicação do bônus de treino        |
| 6   | Adicionar um bônus            | Avaliar clareza dos campos de edição para bônus numéricos                |
| 7   | Subir vida/mana               | Testar manuseio de recursos e clareza entre valores "atuais" e "máximos" |
| 8   | Suba de nível (mesma classe)  | Validar progressão simples e feedback visual de aumento de nível         |
| 9   | Suba de nível (outra classe)  | Testar complexidade da interface multiclasse                             |
| 10  | Adicione uma habilidade       | Avaliar facilidade de encontrar botões de adição na ficha                |
| 11  | Adicione o Homebrew à ficha   | Validar integração entre módulos (Criação vs. Personagem)                |
| 12  | Delete a ficha                | Verificar facilidade de gerenciamento e segurança do fluxo de exclusão   |

## 4. Análise dos Dados e Problemas Encontrados

### Tabela Resumida de Problemas

| N°  | Problema                                             | Tela                      | Gravidade | Esforço |
| --- | ---------------------------------------------------- | ------------------------- | --------- | ------- |
| 1   | Visibilidade dos botões                              | Home                      | Média     | Alto    |
| 2   | Feedback de Input (CapsLock)                         | Login                     | Baixa     | Baixa   |
| 3   | Ambiguidade de Rótulos                               | Ficha                     | Média     | Média   |
| 4   | Fluxo Homebrew (Falha 1ª tentativa)                  | Homebrew                  | Alta      | Média   |
| 5   | Diferenciação Login/Cadastro                         | Login                     | Baixa     | Baixa   |
| 6   | Gestão de Vida/Mana                                  | Ficha                     | Média     | Baixa   |
| 7   | Botão "Salvar" não funciona (Classe HB)              | Criar Homebrew            | Alta      | Médio   |
| 8   | Mensagem de erro ao deletar ficha                    | Meus Personagens          | Média     | Baixa   |
| 9   | Validação sem feedback em tempo real                 | Criar Conta               | Baixa     | Baixa   |
| 10  | Ícones genéricos nas categorias Homebrew (CO4)       | Homebrew - Categorias     | Alta      | Baixo   |
| 11  | Ausência de feedback após criação Homebrew (CO2)     | Homebrew - Criar/Editar   | Alta      | Médio   |
| 12  | Ausência de feedback após atualização de ficha (CO2) | Ficha - Edição            | Alta      | Médio   |
| 13  | Ausência de feedback após exclusão (CO2)             | Homebrew/Ficha - Exclusão | Alta      | Médio   |
| 14  | Ícone de edição pequeno e pouco destacado (AC3)      | Ficha - Visualização      | Média     | Baixo   |
| 15  | Inconsistência de botões (links vs botões) (FM6)     | Homebrew - Listagem       | Alta      | Médio   |
| 16  | Hierarquia visual invertida nos cards (FM2)          | Personagens - Card        | Média     | Baixo   |
| 17  | Falta de indicação de página ativa no menu           | Menu Principal            | Baixa     | Baixa   |

### Detalhamento das Soluções

**Problemas de Alta Gravidade (6):**

- **#4, #7:** Revisar lógica de persistência e formulários Homebrew
- **#10:** Redesenhar ícones com metáforas visuais específicas por categoria
- **#11, #12, #13:** Implementar sistema de notificações toast para todas operações CRUD
- **#15:** Padronizar padrão de botões mantendo hierarquia visual

**Problemas de Média Gravidade (7):**

- **#1:** Aumentar contraste e destaque visual das abas
- **#3:** Inserir labels/placeholders em perícias e atributos
- **#6:** Diferenciar visualmente valor atual vs máximo (Vida/Mana)
- **#8:** Corrigir tratamento de resposta da API ao deletar
- **#14:** Aumentar tamanho e contraste do ícone de edição
- **#16:** Redesenhar hierarquia: primário sólido, destrutivo secundário

**Problemas de Baixa Gravidade (4):**

- **#2:** Adicionar aviso visual de CapsLock ativado
- **#5:** Separar visualmente botões "Entrar" e "Criar Conta"
- **#9:** Adicionar feedback em tempo real sobre requisitos de campos
- **#17:** Adicionar estado ativo no menu de navegação

---

## 5. Análise Estatística/Qualitativa

- **Qualitativa:** Os usuários elogiaram a ideia, a organização visual e o potencial de customização. No entanto, o sistema apresenta problemas críticos de feedback (ausência de confirmações visuais após operações), inconsistência de padrões de interação (botões vs links), e falta de clareza em ícones e navegação, que impactam severamente a experiência do primeiro contato.

- **Quantitativa:** 50% dos usuários (3 de 6) classificaram o sistema como "Fácil" ou superior, enquanto 50% (3 de 6) classificaram como "Regular" ou "Médio". 83% (5 de 6) encontraram dificuldades relacionadas à falta de feedback visual após operações (salvar, excluir), e 67% (4 de 6) relataram problemas com inconsistência de padrões de botões e ícones genéricos. 17 problemas únicos foram identificados, sendo 6 de gravidade Alta (35%), 7 de Média (41%) e 4 de Baixa (24%).

---

## 1. Sujeito: Patrícia

### 1. Equipe da Sessão

- **Condutor:** Agnes Gonçalves Barbosa
- **Recrutador:** Agnes Gonçalves Barbosa

### 2. Perfil do Sujeito

- **Perfil Classificado:** (x) Indiferente
- **Familiaridade com o sistema:** (x) Potencial

### 3. Registros da sessão de avaliação

- **Percepção Inicial:** "Site de ficha pra tormenta."
- **1ª Tarefa:** Problema com CapsLock ativado; sugeriu detector visual.
- **2ª Tarefa:** Demorou a encontrar o botão para homebrew.
- **3ª Tarefa:** Falha ao adicionar conteúdo homebrew na primeira tentativa.
- **4ª Tarefa:** Confusão ao adicionar bônus nas perícias e botão de treino.

### 4. Registros do debrief

1. **Facilidade:** (x) Regular
2. **Satisfação:** (x) Indiferente
3. **Clareza:** (x) Razoável
4. **Pontos Positivos:** Aba de Homebrew intuitiva após ser localizada.
5. **Pontos de Melhoria:** Falta de indicação visual e dificuldade em achar abas pela primeira vez.

### 5. Problemas encontrados

| N°  | Problema                   | Tela             | Gravidade | Esforço | Possível Solução                                                    |
| --- | -------------------------- | ---------------- | --------- | ------- | ------------------------------------------------------------------- |
| 1   | Visibilidade dos botões    | Home             | Média     | Alto    | Alterar cores para aumentar contraste e destaque.                   |
| 2   | Falta de feedback de input | Login/Cadastro   | Baixa     | Baixa   | Aviso visual para CapsLock ativado.                                 |
| 3   | Ambiguidade na edição      | Ficha (Perícias) | Média     | Média   | Adicionar rótulos (labels) ou placeholders claros.                  |
| 4   | Fluxo de Adição Homebrew   | Homebrew         | Alta      | Média   | Revisar lógica de confirmação para garantir adição na 1ª tentativa. |

---

## 2. Sujeito: Felipe

### 1. Equipe da Sessão

- **Condutor:** Agnes Gonçalves Barbosa
- **Recrutador:** Agnes Gonçalves Barbosa

### 2. Perfil do Sujeito

- **Perfil Classificado:** (x) Apoiador
- **Familiaridade com o sistema:** (x) Potencial

### 3. Registros da sessão de avaliação

- **Percepção Inicial:** "Site de ficha pra tormenta."
- **Tarefa 1:** Errou ao tentar criar conta usando o campo de "entrar".
- **Tarefa 2:** Conseguiu criar e excluir Homebrew, mas não conseguiu editar.
- **Tarefa 3:** Criou a ficha com sucesso.
- **Tarefa 4:** Dificuldade ao adicionar uma habilidade específica.

### 4. Registros do debrief

1. **Facilidade:** (x) Fácil
2. **Satisfação:** (x) Satisfeito
3. **Clareza:** (x) Claras
4. **Pontos Positivos:** Espaços para customização, intuitivo e fichas organizadas.
5. **Pontos de Melhoria:** Incompatibilidade com modo escuro do Chrome.

### 5. Problemas encontrados

| N°  | Problema                   | Tela             | Gravidade | Esforço | Possível Solução                                               |
| --- | -------------------------- | ---------------- | --------- | ------- | -------------------------------------------------------------- |
| 1   | Fluxo de entrada incorreto | Login / Cadastro | Baixa     | Baixa   | Diferenciar visualmente os botões de "Entrar" e "Criar Conta". |
| 2   | Impedimento na edição      | Homebrew         | Média     | Média   | Corrigir a funcionalidade de edição de conteúdos Homebrew.     |
| 3   | Dificuldade de inserção    | Habilidades      | Média     | Baixa   | Revisar o componente de adição de habilidades.                 |
| 4   | Incompatibilidade visual   | Geral            | Baixa     | Baixa   | Ajustar o CSS para suporte ao modo escuro nativo.              |

---

## 3. Sujeito: Ana

### 1. Equipe da Sessão

- **Condutor:** Agnes Gonçalves Barbosa
- **Recrutador:** Agnes Gonçalves Barbosa

### 2. Perfil do Sujeito

- **Perfil Classificado:** (x) Apoiador
- **Familiaridade com o sistema:** (x) Potencial

### 3. Registros da sessão de avaliação

- **Percepção Inicial:** Fazer ficha de Tormenta.
- **Tarefa 1:** Cadastro realizado sem dificuldades.
- **Tarefa 2:** Homebrew criado e adicionado sem problemas.
- **Tarefa 3:** Uso fluído dos botões de atributos.

### 4. Registros do debrief

1. **Facilidade:** (x) Muito Fácil
2. **Satisfação:** (x) Muito Satisfeito
3. **Clareza:** (x) Muito claras
4. **Pontos Positivos:** Interface geral intuitiva e ficha fácil de mexer.
5. **Pontos de Melhoria:** Adicionar informações básicas sobre o sistema Tormenta (ex: nº de atributos).

### 5. Problemas encontrados

| N°  | Problema                    | Tela    | Gravidade | Esforço | Possível Solução                                              |
| --- | --------------------------- | ------- | --------- | ------- | ------------------------------------------------------------- |
| 1   | Falta de auxílio contextual | Criação | Baixa     | Baixa   | Incluir tooltips ou informativos sobre as regras de Tormenta. |

---

## 4. Sujeito: Eydson

### 1. Equipe da Sessão

- **Condutor:** Agnes Gonçalves Barbosa
- **Recrutador:** Agnes Gonçalves Barbosa

### 2. Perfil do Sujeito

- **Perfil Classificado:** (x) Apoiador
- **Familiaridade com o sistema:** (x) Potencial

### 3. Registros da sessão de avaliação

- **Percepção Inicial:** Site para criar e gerenciar fichas de T20.
- **Tarefa 1:** Criou raça com sucesso.
- **Tarefa 2:** Adicionou homebrew com facilidade.
- **Tarefa 3:** Confusão visual com os campos de Mana e Vida.
- **Tarefa 4:** Demora em localizar a opção de adicionar habilidades.

### 4. Registros do debrief

1. **Facilidade:** (x) Fácil
2. **Satisfação:** (x) Satisfeito
3. **Clareza:** (x) Claras
4. **Pontos Positivos:** Praticidade na criação de Homebrews e layout em 3 colunas.
5. **Pontos de Melhoria:** Ausência de cabeçalhos em tabelas e dificuldade em distinguir PV atual/máximo.

### 5. Problemas encontrados

| N°  | Problema                | Tela              | Gravidade | Esforço | Possível Solução                                                      |
| --- | ----------------------- | ----------------- | --------- | ------- | --------------------------------------------------------------------- |
| 1   | Ambiguidade de status   | Ficha (Vida/Mana) | Média     | Baixa   | Clarificar visualmente qual campo é o "Atual" e qual é o "Máximo".    |
| 2   | Localização de recursos | Ficha             | Média     | Baixa   | Melhorar destaque do botão de adição de habilidades.                  |
| 3   | Ausência de cabeçalhos  | Perícias          | Média     | Baixa   | Adicionar rótulos indicando bônus e proficiência nas colunas.         |
| 4   | Lentidão no Level Up    | Ficha             | Baixa     | Média   | Permitir "settar" o nível manualmente para personagens de nível alto. |

---

## 5. Sujeito: Henrique

### 1. Equipe da Sessão

- **Condutor:** Nathan Cavalcante
- **Recrutador:** Nathan Cavalcante

### 2. Perfil do Sujeito

- **Perfil Classificado:** (x) Indiferente
- **Familiaridade com o sistema:** (x) Primeiro Contato

### 3. Registros da sessão de avaliação

- **Percepção Inicial:** "Site para gerenciar fichas de Tormenta 20."
- **1ª Tarefa:** Confusão inicial entre "Entrar" e cadastro. Erros de validação por campos muito curtos.
- **2ª Tarefa:** Botão "Salvar" não funcionou ao criar Classe Homebrew (Ladino). Criou Raça (Anão) com sucesso.
- **3ª Tarefa:** Acessou lista de homebrews com sucesso.
- **4ª Tarefa:** Criou ficha (Lido, Elfo, Ladino) sem dificuldades.
- **5ª Tarefa:** Adicionou treino nas perícias com sucesso.
- **6ª Tarefa:** Adicionou bônus manualmente com sucesso.
- **7ª Tarefa:** Subiu vida/mana usando botões de incremento.
- **8ª Tarefa:** Subiu nível da classe principal (Ladino) através do modal.
- **9ª Tarefa:** Adicionou nova classe usando "Adicionar Classe" no modal.
- **10ª Tarefa:** Adicionou habilidade "Conhecimento das Rochas" com sucesso.
- **11ª Tarefa:** Integrou homebrew "Muito Alto" à ficha.
- **12ª Tarefa:** Mensagem de erro (toast vermelho) ao deletar ficha. Comentário: "Deu um erro".

### 4. Registros do debrief

1. **Facilidade:** (x) Regular
2. **Satisfação:** (x) Indiferente
3. **Clareza:** (x) Claras
4. **Pontos Positivos:** "O que eu gostei é o potencial de customizar o que quiser com certa facilidade e uma UI que parece bem simples, limpa e direta"
5. **Pontos de Melhoria:** "E melhorar é colocar algo mais de 'decoração' e fazer com que realmente adicione as informações na ficha."

### 5. Problemas encontrados

| N°  | Problema                                                                                       | Tela             | Gravidade | Esforço | Possível Solução                                                                   |
| --- | ---------------------------------------------------------------------------------------------- | ---------------- | --------- | ------- | ---------------------------------------------------------------------------------- |
| 1   | Botão "Salvar" não funciona ao tentar criar uma Classe Homebrew                                | Criar Homebrew   | Alta      | Médio   | Depurar o evento de submit do formulário de criação de classe.                     |
| 2   | Mensagem de erro (Toast vermelho) aparece ao deletar a ficha, mesmo com a ação sendo concluída | Meus Personagens | Média     | Baixo   | Corrigir o tratamento de resposta da API na função de deletar.                     |
| 3   | Validação de campos (Login/Senha) só avisa sobre tamanho mínimo após tentativa de envio        | Criar Conta      | Baixa     | Baixo   | Adicionar feedback em tempo real ou instrução visual sobre o mínimo de caracteres. |

---

## 6. Sujeito: João Ricardo Campêlo Silva

### 1. Equipe da Sessão

- **Condutor:** Lucas Pinheiro da Costa
- **Recrutador:** Lucas Pinheiro da Costa

### 2. Perfil do Sujeito

- **Nome:** João Ricardo Campêlo Silva
- **Experiência com RPG:** Joga D&D há 4 anos, nunca jogou Tormenta 20
- **Perfil Classificado:** (X) Apoiador
- **Familiaridade com o Sistema:** (X) Primeiro contato

### 3. Registros da sessão de avaliação

#### 3.1 Pergunta Inicial: "Ao observar a tela principal, para que serve o aplicativo?"

"Pelo título 'Arkheion', parece ser algo relacionado a RPG. Tem ali 'Ver minhas fichas' e 'Criar nova ficha', então acho que é um sistema para criar fichas de RPG. Nesse canto que diz 'Crie e gerencie fichas de personagem para Tormenta 20' tá mencionando o sistema Tormenta 20 que eu já ouvi falar dele, mas não conheço direito porque nunca utilizei, sabe? Mas acredito que seja parecido com D&D. Tem também um menu ali em cima com 'Homebrew' e 'Personagens'... não sei o que é Homebrew, nunca usei em RPG, mas no geral é isso, é sobre ficha de RPG, só não sei como o sistema funciona."

#### 3.2 Tarefa 01: Navegação e identificação de categoria

**Instrução dada:** "Você é um mestre de RPG e deseja criar uma raça personalizada para a sua campanha. Encontre a seção de conteúdos personalizados (Homebrew) e inicie o processo para criar uma nova Raça."

**Problemas observados:**

- Hesitação ao identificar as categorias devido aos ícones genéricos
- Comentário sobre inconsistência visual do botão de criação

#### 3.3 Tarefa 02: Criação e persistência de dados

**Instrução dada:** "Preencha o nome da raça como 'Elfo da Lua' e finalize a criação, salvando o seu novo conteúdo no sistema."

**Problemas observados:**

- Falta de feedback visual após salvar causou 5 segundos de hesitação
- Necessidade de retornar à listagem para confirmar que a ação foi bem-sucedida

#### 3.4 Tarefa 03: Aplicação da raça homebrew na ficha de personagem

**Instrução dada:** "Acesse a ficha do personagem 'Conan', edite o campo 'Raça' e selecione a opção 'Elfo da Lua' no dropdown. Salve a ficha de personagem para confirmar a alteração."

**Problemas observados:**

- Novamente, falta de feedback após salvar

#### 3.5 Tarefa 04: Gestão de conteúdo (edição/exclusão)

**Instrução dada:** "Localize a raça que você acabou de criar na sua lista de 'Meus Homebrews' e exclua ela permanentemente do sistema."

**Problemas observados:**

- Inconsistência com o padrão de botões usado em outras telas
- Falta de feedback após exclusão

#### 3.6 Tarefa 05: Recuperação de navegação (caminho de volta)

**Instrução dada:** "Saia da área de Homebrew e retorne para o Painel Principal (Dashboard) do sistema."

**Problemas observados:**

- Falta de indicação visual de página ativa no menu

#### 3.7 Tarefa 06: Limpeza do sistema (exclusão da ficha)

**Instrução dada:** "Acesse a lista de personagens e execute a exclusão permanente da ficha do 'Conan'. Confirme que o personagem desapareceu da sua lista."

**Problemas observados:**

- Falta de feedback positivo após exclusão bem-sucedida

### 4. Registros do Debrief

1. **Como você avalia a facilidade de realizar as tarefas propostas no sistema?**
   - "Eu diria que foi médio. Dá pra fazer as coisas, mas tem muita coisa que deixa você confuso. Os ícones são bem parecidos, os botões às vezes são links de texto, às vezes são botões de verdade... você fica meio perdido. Mas o que me incomodou também foi a falta de mensagem explicando se a ação deu certo ou não."
   - **Classificação:** (X) Médio

2. **De modo geral, quão satisfeito você se sentiu ao usar este sistema?**
   - "É ok, dá pro gasto de mexer com uma ficha de RPG, mas precisa melhorar algumas funcionalidades pra ficar realmente adequado, sabe? Nesse aspecto, fazer as anotações de papel ainda é mais prático, mas eu vejo um grande potencial nesse sistema."
   - **Classificação:** (X) Indiferente

3. **As informações na tela estavam claras e fáceis de entender?**
   - "Não muito claras… Os rótulos estão ok, tipo 'Raças', 'Classes', mas os ícones não ajudam em nada. E não ter feedback nas ações deixa tudo muito ambíguo. Eu sempre ficava na dúvida: 'salvou?', 'excluiu?', 'deu certo?'."
   - **Classificação:** (X) Pouco claras

4. **O que você mais gostou no sistema?**
   - "Gostei que a janelinha pequena de confirmação aparece antes de você excluir mesmo. Isso evita que você delete algo sem querer. E gostei que a listagem de personagens tem os cards com foto e informações básicas, fica organizado."

5. **O que você menos gostou no sistema?**
   - "Algumas mensagens de confirmação que deveriam dizer que sua ação foi executada com sucesso ou algo do tipo, sabe? Toda vez que eu salvava ou excluía, ficava aquela sensação de 'será que funcionou?'. E os botões muito inconsistentes também. Às vezes é um botão cheio, às vezes é só um textinho. E aqueles ícones quadradinhos genéricos das categorias de Homebrew não servem pra nada"

6. **Você recomendaria este sistema para outros jogadores de RPG?**
   - "No estado atual, provavelmente não. Ele funciona, mas falta polimento. Mas se essas questões de feedback e consistência forem consertadas, aí sim poderia virar uma boa opção."

### 5. Problemas encontrados

| N°  | Problema                                                                                                                                                                                   | Tela                      | Gravidade | Esforço |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------- | --------- | ------- |
| 1   | Ícones genéricos e não representativos nas categorias de Homebrew (Raças, Classes, Poderes, Itens) dificultam a identificação visual e violam a diretriz de metáfora visual adequada (CO4) | Homebrew - Categorias     | Alta      | Baixo   |
| 2   | Ausência total de feedback visual (toast, notificação, mensagem) após operações de criação de entidades Homebrew, violando a diretriz de feedback adequado (CO2)                           | Homebrew - Criar/Editar   | Alta      | Médio   |
| 3   | Ausência de feedback visual após operações de atualização em fichas de personagem, gerando insegurança sobre o sucesso da operação (CO2)                                                   | Ficha - Edição            | Alta      | Médio   |
| 4   | Ausência de feedback visual após operações de exclusão de entidades Homebrew e fichas de personagem (CO2)                                                                                  | Homebrew/Ficha - Exclusão | Alta      | Médio   |
| 5   | Ícone de edição (lápis) na visualização da ficha é pequeno e pouco destacado, causando dificuldade de localização (AC3)                                                                    | Ficha - Visualização      | Média     | Baixo   |
| 6   | Links de texto ("Editar" / "Excluir") nos cards de Homebrew não seguem o padrão de botões sólidos usado em outras telas (ex: Personagens), violando consistência interna (FM6)             | Homebrew - Listagem       | Alta      | Médio   |
| 7   | Hierarquia visual inadequada no card de personagem: botão destrutivo ("Excluir ficha") tem destaque maior que a ação primária ("Acessar ficha"), invertendo a importância das ações (FM2)  | Personagens - Card        | Média     | Baixo   |
