# CDU010. Subir de Nível.

- **Ator principal**: Usuário
- **Atores secundários**: ---
- **Resumo**: O usuário sobe de nível.
- **Pré-condição**: ---
- **Pós-Condição**: ---

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - Entra na tela de personagem. | 2 - Exibe a tela de Personagem. |  
| 3 - Clica na opção de vizualização de ficha de personagem. | 4 - Exibe a tela de ficha já devidamente preenchida. |
| 5 - Clica na caixa de edição do perfil de personagem. | 6 - Mostra a tela de edição dos dados de personagem. |
| 7 - Clica na caixinha numérica para subir de nível e confirma a edição. | 8 - Salva o novo nível e exibe a ficha com os novos cálculos de perícia. |

## Fluxo Alternativo I - Caractere Inválido.
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: |   
| 7.1 - Clica para editar o número manualmente e preenche os dados incorretamente, com caracteres inválidos. | 8.1 - Envia um aviso de caractere inválido, pedindo para que tente novamente. A ação se repete até que os dados sejam inseridos corretamente ou que a ação seja cancelada. |
| 9.1 - Insere os dados corretamente. | 10.1 - Autentica os dados e volta para a página de vizualização de ficha com o valor do atributo atualizada. |

## Diagrama de Interação (Sequência ou Comunicação)

```mermaid
sequenceDiagram
    participant Usuario
    participant SubirNivelView
    participant NivelClasseFicha
    participant Ficha

    Usuario ->> SubirNivelView: EscolherSubirNivelView.get
    SubirNivelView -->> Usuario: render('escolher_subir_nivel.html')
    Usuario ->> SubirNivelView: SubirNivelClasseAtualView.post
    SubirNivelView ->> NivelClasseFicha: NivelClasseFicha.objects.filter
    NivelClasseFicha -->> SubirNivelView: Retorna nível atual
    SubirNivelView ->> NivelClasseFicha: nivel_classe.nivel += 1
    NivelClasseFicha ->> Ficha: ficha.nivel += 1
    Ficha -->> NivelClasseFicha: Confirma atualização
    NivelClasseFicha -->> SubirNivelView: Confirma aumento de nível
    SubirNivelView -->> Usuario: redirect('ficha_combate')
```

## Diagrama de Classes de Projeto

```mermaid
classDiagram

    namespace django.contrib.auth{
        class Usuario {
            <<Django Model>>
        }
    }

    class Ficha {
        +id: Integer
        +nome: CharField
        +nivel: Integer
        +subirUmNivel()
        +setarNivel()
        +calcular_todas_pericias()
        +calcularVida()
        +calcularMana()
    }

    class Atributo {
        +id: Integer
        +nome: CharField
    }

    class AtributoFicha {
        +id: Integer
        +valor: Integer
    }

    class Pericia {
        +id: Integer
        +nome: CharField
        +requerTreino: Boolean
    }

    class PericiaTreinada {
        +id: Integer
        +treinado: Boolean
        +calcularValor()
        +verificarTreino()
        +adicionarBonus()
    }

    class NivelClasseFicha {
        +id: Integer
        +nivel: Integer
        +vida_por_nivel: Integer
        +mana_por_nivel: Integer
        +subirNivel()
    }

    class SubirNivelView {
        +get()
        +post()
    }

    Usuario "1" *--> "*" Ficha
    Ficha "1" *--> "*" AtributoFicha
    AtributoFicha "*" *--> "1" Atributo
    Ficha "1" *--> "*" PericiaTreinada
    PericiaTreinada "*" *--> "1" Pericia
    PericiaTreinada "*" *--> "1" AtributoFicha
    Ficha "1" *--> "*" NivelClasseFicha
    NivelClasseFicha "*" *--> "1" Ficha
    NivelClasseFicha "1" *--> "*" PericiaTreinada
    SubirNivelView "*" *--> "1" NivelClasseFicha
```
