# CDU004. Utilizar Perícias.

- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário usa uma ficha de personagem.
- **Pré-condição**: Estar logado; ter uma ficha já feita e editada.
- **Pós-Condição**: ---

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: |
| 1 - Entra na tela de personagem. | 2 - Exibe a tela de Personagem. |  
| 3 - Clica na opção de vizualização de ficha de personagem. | 4 - Exibe a tela de ficha já devidamente preenchida. |
| 5 - Escolhe, dentre as opções de períciais, uma para usar, e clica em cima dela.| 6 - Exibe o resultado do teste requisitado, já com o dado(d20) somado aos devidos bônus. |

## Fluxo Alternativo I - Perícia rotulada como "Somente treinada".
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: | 
| 5.1 - Escolhe, dentre as opções de períciais, uma para usar das rotuladas como "Somente treinadas", e clica em cima dela.| 6.1 - Mostra um aviso de que só é possível utilizar a especificada perícia se o personagem for treinado. |

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

> Substituir pela imagem correspondente...

## Diagrama de Classes de Projeto

> Substituir pela imagem contendo as classes (modelo, visão e templates) que implementam o respectivo CDU...