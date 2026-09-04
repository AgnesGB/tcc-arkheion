# CDU003. Excluir Ficha de Personagem.

- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário exclui uma ficha de personagem.
- **Pré-condição**: Estar logado; ter uma ficha já feita.
- **Pós-Condição**: Ficha de Personagem é excluída.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - Entra na tela de personagem. | 2 - Mostra a tela de  Personagem. |  
| 3 - Clica na opção "Excluir ficha". | 4 - Mostra a tela pedindo confirmação se deseja realmente excluir a ficha, pedindo confirmação de senha. |
| 5 - Insere os dados e prossegue com a ação de exclusão. | 6 - Mostra que a ficha foi excluida com sucesso. | 

## Fluxo Alternativo I - Senha incorreta.
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: | 
| 3.1 - Clica na opção "Excluir ficha". | 4.1 - Mostra a tela pedindo confirmação se deseja realmente excluir a ficha, pedindo confirmação de senha. |
| 5.1 - Insere os dados incorretamente. | 6.1 - Envia um aviso de senha incorreta, pedindo para que tente novamente. A ação se repete até que os dados sejam inseridos corretamente. |
| 7.1 - Insere os dados corretamente e prossegue com a ação de exclusão. | 8.1 - Mostra que a ficha foi excluida com sucesso. | 

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

> Substituir pela imagem correspondente...

## Diagrama de Classes de Projeto

> Substituir pela imagem contendo as classes (modelo, visão e templates) que implementam o respectivo CDU...
