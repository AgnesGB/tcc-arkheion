# Relatório Final de Avaliação de Usabilidade

**Projeto:** Arkheion 
* **Data de Conclusão:** 22/12/2025 
* **Responsável:** Agnes Gonçalves Barbosa 

## Roteiro de Tarefas da Avaliação

Durante a sessão, cada sujeito foi orientado a realizar as seguintes ações no sistema para testar a navegabilidade e funcionalidade:

1. **Criação de Acesso:** Realizar o cadastro de uma nova conta no sistema.

2. **Gestão de Conteúdo Customizado (Homebrew):**
* Criar um novo conteúdo do tipo Homebrew.
* Acessar a listagem de Homebrews criados.

3. **Configuração de Personagem:**
* Criar uma nova ficha de personagem.
* Adicionar o conteúdo Homebrew previamente criado à ficha de personagem.

4. **Edição de Perícias e Atributos:**
* Marcar o treinamento em perícias específicas.
* Adicionar bônus numéricos aos campos da ficha.

5. **Gerenciamento de Recursos e Progressão:**
* Alterar manualmente os valores de Vida e Mana.
* Subir o nível do personagem na classe principal.
* Realizar o "multiclasse" (subir nível em uma classe diferente).
* Adicionar novas habilidades à ficha de personagem.

6. **Finalização:** Excluir a ficha de personagem criada.


## 1. Resumo Executivo

O sistema foi bem recebido pela maioria dos usuários, sendo descrito como intuitivo e organizado. No entanto, foram identificados pontos críticos de atrito no fluxo de login/cadastro, na visibilidade de botões principais e na clareza de rótulos dentro da ficha de personagem.

## 2. Métricas de Satisfação (Média dos Usuários)

| Critério | Avaliação Predominante |
| --- | --- |
| **Facilidade de Uso** | Fácil a Regular |
| **Satisfação Geral** | Satisfeito / Muito Satisfeito |
| **Clareza de Informação** | Claras a Razoável |

---

## 3. Principais Descobertas e Pontos de Dor

### A. Interface e Navegação

* **Contraste e Visibilidade:** Usuários tiveram dificuldade em localizar abas (como Homebrew) devido ao baixo contraste visual dos botões.
* **Modo Escuro:** Foi reportada incompatibilidade visual com o modo escuro nativo do navegador Chrome.

### B. Fluxo de Cadastro e Login

* **Erros de Entrada:** Confusão entre os campos de "Entrar" e "Criar Conta".
* **Feedback de Teclado:** Ausência de aviso para o CapsLock ativado, prejudicando o preenchimento de senhas.

### C. Gestão de Fichas e Homebrew

* **Ambiguidade de Dados:** Falta de rótulos claros em tabelas de perícias e na distinção entre valores atuais e máximos de Vida/Mana.
* **Persistência de Dados:** O sistema apresentou falhas pontuais ao salvar conteúdos Homebrew na primeira tentativa.
* **Funcionalidades de Edição:** Usuários conseguiram criar e excluir itens, mas encontraram bloqueios ao tentar editar Homebrews já existentes.

---

## 4. Recomendações de Melhoria (Priorizadas)

### Prioridade Alta (Corrigir Imediatamente)

1. **Rótulos e Cabeçalhos:** Implementar cabeçalhos em todas as tabelas (Perícias, Habilidades) e identificar claramente os campos de edição.
2. **Correção de Fluxo:** Garantir que o botão de confirmação do Homebrew funcione na primeira tentativa.
3. **Diferenciação Visual:** Tornar os botões de navegação principal (Homebrew, Criar Ficha) mais destacados.

### Prioridade Média (Evolução do Sistema)

1. **Feedback Visual:** Adicionar detecção de CapsLock no login.
2. **Edição de Conteúdo:** Habilitar a função de edição para conteúdos Homebrew.
3. **UX de Level Up:** Adicionar uma função para definir o nível do personagem manualmente, evitando múltiplos cliques no botão de "subir nível".

### Prioridade Baixa (Ajustes Finos)

1. **Modo Escuro:** Ajustar o CSS para compatibilidade com temas escuros.
2. **Ajuda Contextual:** Adicionar tooltips com informações básicas das regras de Tormenta para auxiliar utilizadores potenciais.

---

## 5. Conclusão

O produto possui uma base sólida e foi elogiado pela sua organização visual. Os problemas encontrados são, em sua maioria, ajustes de interface (UI) e clareza textual (UX Writing). A correção das ambiguidades na ficha de personagem é o passo mais importante para garantir uma experiência fluida para jogadores veteranos e novatos.

---

### 6. Decisão Estratégica: Refatoração do Front-end

**Conclusão:** O sistema é funcional, mas carece de robustez na interface de usuário (UI). As hipóteses de que o sistema seria totalmente intuitivo foram parcialmente refutadas pelas dificuldades em tarefas de edição e localização de abas.

**Decisão: Refatoração do Front-end**
A partir das evidências, a equipe decidiu pela refatoração total do front-end com foco em:

* **Redesign do Sistema de Cores e Contraste:** Implementação de uma nova paleta para aumentar a visibilidade de botões críticos e abas, corrigindo a dificuldade de localização relatada.
* **Padronização de Rótulos e Tabelas:** Adição sistemática de cabeçalhos e rótulos (labels) em todas as áreas de edição, especialmente na ficha de perícias e status de Vida/Mana, para eliminar ambiguidades.
* **Otimização do Fluxo de Login e Cadastro:** Reestruturação visual da tela de entrada para diferenciar claramente as ações de "Entrar" e "Criar Conta", prevenindo erros de percurso inicial.
* **Arquitetura de Componentes de Edição:** Refatoração da lógica de interação com conteúdos Homebrew para garantir que a edição seja funcional e que adições não falhem na primeira tentativa.
* **Suporte Nativo a Temas (Dark Mode):** Ajuste da folha de estilos (CSS) para garantir compatibilidade total com o modo escuro, evitando quebras visuais em navegadores.