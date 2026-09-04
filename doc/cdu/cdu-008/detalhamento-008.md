# CDU008. Adicionar bônus de perícia.

- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário adiciona um bônus a uma perícia.
- **Pré-condição**: ---
- **Pós-Condição**: ---

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - Entra na tela de personagem. | 2 - Exibe a tela de Personagem. |  
| 3 - Clica na opção de vizualização de ficha de personagem. | 4 - Exibe a tela de ficha já devidamente preenchida. |
| 5 - Escolhe, dentre as opções de períciais, uma pericia para adicionar o bônus, digita o valor desejado. | 6 - Atualiza o valor da perícia automaticamente. |

## Fluxo Alternativo I - Caractere Inválido.
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: |   
| 5.1 - Preenche os dados nos campos informados incorretamente, com caracteres inválidos. | 6.1 - Envia um aviso de caractere inválido, pedindo para que tente novamente. A ação se repete até que os dados sejam inseridos corretamente. |
| 7.1 - Insere os dados corretamente. | 8.1 - Atualiza o valor da perícia automaticamente. |

## Fluxo Alternativo II - Botões.
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: |   
| 5.2 - Clica no botãozinho no campo indicado. | 6.2 - Atualiza o valor da perícia automaticamente de um em um. |


## Diagrama de Interação (Sequência)

```mermaid
sequenceDiagram
    actor Usuário
    participant PersonagensView
    participant FichaCombateView
    participant AtualizarBonusView
    participant Ficha
    participant PericiaTreinada

    Usuário->>+PersonagensView: 1: GET /personagens
    PersonagensView->>PersonagensView: 1.1: Prepara contexto
    PersonagensView-->>-Usuário: 1.2: Renderiza personagens.html

    Usuário->>+FichaCombateView: 2: GET /ficha_combate/{ficha_id}
    FichaCombateView->>+Ficha: 2.1: Busca ficha
    Ficha-->>-FichaCombateView: 2.2: Retorna ficha
    FichaCombateView-->>-Usuário: 2.3: Renderiza ficha_combate.html

    alt Atualização de Bônus
        Usuário->>+AtualizarBonusView: 3: POST /atualizar_bonus/{ficha_id}
        activate AtualizarBonusView

        alt Sucesso
            AtualizarBonusView->>+PericiaTreinada: 3.1: Busca perícia
            PericiaTreinada-->>-AtualizarBonusView: 3.2: Retorna perícia
            AtualizarBonusView->>PericiaTreinada: 3.3: Atualiza bônus
            AtualizarBonusView->>PericiaTreinada: 3.4: Salva alterações
            AtualizarBonusView-->>Usuário: 3.5: Retorna JSON (sucesso)
        else Erro
            AtualizarBonusView-->>Usuário: 3.6: Retorna JSON (erro)
            loop Tentativas
                Usuário->>AtualizarBonusView: 3.7: POST novamente
                AtualizarBonusView->>PericiaTreinada: 3.8: Processa atualização
                AtualizarBonusView-->>Usuário: 3.9: Retorna sucesso
            end
        end

        deactivate AtualizarBonusView
        Usuário->>+FichaCombateView: 4: GET /ficha_combate/{ficha_id}
        FichaCombateView->>Ficha: 4.1: Busca ficha atualizada
        Ficha-->>FichaCombateView: 4.2: Retorna dados
        FichaCombateView-->>-Usuário: 4.3: Renderiza atualizado
    end
```

## Diagrama de Classes de Projeto

```mermaid
classDiagram
    class AtualizarBonusView {
        +post()
    }

    namespace django.contrib.auth{
        class User {
            <<Django Model>>
        }
    }

    class Ficha {
        +id: Integer
        +nome: CharField
        +nivel: Integer
        +calcularVida()
        +calcularMana()
        +calcular_todas_pericias(): dict
    }

    class Pericia {
        +id: Integer
        +nome: CharField
        +requer_treino: Boolean
    }

    class PericiaTreinada {
        +id: Integer
        +ficha: ForeignKey(Ficha)
        +pericia: ForeignKey(Pericia)
        +bonus_adicional: Integer
        +verificarTreino(): int
        +calcularValor(): int
        +adicionarBonus(valor: int): void
    }

    AtualizarBonusView "*" *--> "1" PericiaTreinada 
    Ficha "*" o--> "*" PericiaTreinada
    PericiaTreinada "*" o--> "1" Pericia
    Ficha "1" *--> "1" User 

```
