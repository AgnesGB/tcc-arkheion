# CDU002. Editar Ficha de Personagem
- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário edita a sua ficha de personagem.
- **Pré-condição**: Estar logado; ter a ficha criada.
- **Pós-Condição**: A ficha é editada.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - Entra na tela de personagem. | 2 - Mostra a tela de  Personagem. |  
| 3 - Escolher a ficha desejada para edição. | 4 - Mostra a tela de ficha. | 
| 5 - Escolhe qual campo deseja editar: Informações básicas, ataques, habilidades, magias(se houver), equipamentos ou descrição. | 6 - Mostra o que pode ser editado.
| 7 - Adiciona as informações editadas. | 8 - Mostra a ficha preenchida com os dados fornecidos. | 

## Fluxo Alternativo I - Ficha de nível diferente do 1.
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 5.1 - Escolhe editar o nível e coloca um nível diferente do 1. | 6.1 - Mostra a ficha atualizada de acordo com o número fornecido e opções para a escolha de poderes dispoíveis ao nível correspondente ao informado. | 
| 7.1 - Escolhe os poderes, habilidades ou magias relativas a cada nível informado.  | 8.1 - Mostra a ficha preenchida com os dados fornecidos. | 

## Fluxo Alternativo II - Nível informado inválido.
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 5.2 - Escolhe editar o nível e informa um número fora do limite de 1-20, ou um caracter não numérico. | 6.2 - Mostra uma mensagem de erro, informando para escolher um número valido ou apenas caracteres numéricos. | 
| 7.2 - Escolhe um nível válido  | 8.2 - Mostra a ficha preenchida com os dados fornecidos, caso o nível informado for diferente de "1", inicia o Fluxo Alternativo I. |   

## Fluxo Alternativo III - Atributos inválidos.
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 5.3 - Escolhe editar os atributos e informa um número que ultrapasse a quantidade permitida de acordo com a distribuição de pontos disponível, ou um carácter não numérico. | 6.3 - Mostra uma mensagem de erro, informando para escolher um número válido ou apenas caracteres numéricos. | 
| 7.3 - Informa os atributos válidos  | 8.3 - Mostra a ficha preenchida com os dados fornecidos, caso o nível informado for diferente de "1", inicia o Fluxo Alternativo I. |   

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

> Substituir pela imagem correspondente...

## Diagrama de Classes de Projeto

> Substituir pela imagem contendo as classes (modelo, visão e templates) que implementam o respectivo CDU...
